from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from datetime import timedelta
from tool.models import InvitationCode
from account.models import EmailVerificationCode


class Command(BaseCommand):
    help = 'Clean up expired invitation codes and email verification codes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--email-used-grace-minutes',
            type=int,
            default=1,
            help='Minutes to wait after email verification is used before deletion (default: 1)',
        )
        parser.add_argument(
            '--email-max-age-minutes',
            type=int,
            default=10,
            help='Maximum age for email verification codes in minutes (default: 10)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        email_used_grace = options['email_used_grace_minutes']
        email_max_age = options['email_max_age_minutes']
        
        now = timezone.now()
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be deleted'))
        
        # Clean up InvitationCode records
        invitation_deleted = self.cleanup_invitation_codes(now, dry_run)
        
        # Clean up EmailVerificationCode records
        email_deleted = self.cleanup_email_verification_codes(
            now, email_used_grace, email_max_age, dry_run
        )
        
        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'Cleanup completed: {invitation_deleted} invitation codes, '
                f'{email_deleted} email verification codes {"would be " if dry_run else ""}deleted'
            )
        )

    def cleanup_invitation_codes(self, now, dry_run=False):
        # Find exhausted codes first (simpler query)
        exhausted_codes = InvitationCode.objects.filter(
            remain_uses=0, 
            max_uses__gt=0
        )
        
        # Find expired codes (need to check each one individually)
        potentially_expired = InvitationCode.objects.filter(
            valid_duration_minutes__gt=0
        )
        
        expired_ids = []
        for code in potentially_expired:
            expiry_time = code.created_at + timedelta(minutes=code.valid_duration_minutes)
            if now > expiry_time:
                expired_ids.append(code.id)
        
        expired_codes = InvitationCode.objects.filter(id__in=expired_ids)
        
        # Combine the querysets
        all_codes_to_delete = exhausted_codes.union(expired_codes)
        
        count = all_codes_to_delete.count()
        
        if count > 0:
            self.stdout.write(f'Found {count} expired/exhausted invitation codes')
            if not dry_run:
                all_codes_to_delete.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted {count} invitation codes'))
            else:
                for code in all_codes_to_delete[:5]:  # Show first 5 as example
                    self.stdout.write(f'  Would delete: {code.code} (server: {code.server.name})')
                if count > 5:
                    self.stdout.write(f'  ... and {count - 5} more')
        else:
            self.stdout.write('No expired invitation codes found')
            
        return count

    def cleanup_email_verification_codes(self, now, used_grace_minutes, max_age_minutes, dry_run=False):
        
        # Find codes to delete
        codes_to_delete = EmailVerificationCode.objects.filter(
            models.Q(
                # Used codes older than grace period
                models.Q(is_used=True) &
                models.Q(used_date__lt=now - timedelta(minutes=used_grace_minutes))
            ) |
            # Codes older than max age regardless of use
            models.Q(created_at__lt=now - timedelta(minutes=max_age_minutes))
        )
        
        count = codes_to_delete.count()
        
        if count > 0:
            self.stdout.write(f'Found {count} expired email verification codes')
            if not dry_run:
                codes_to_delete.delete()
                self.stdout.write(self.style.SUCCESS(f'Deleted {count} email verification codes'))
            else:
                for code in codes_to_delete[:5]:  # Show first 5 as example
                    reason = "used + grace period" if code.is_used else "max age exceeded"
                    self.stdout.write(f'  Would delete: {code.email} ({reason})')
                if count > 5:
                    self.stdout.write(f'  ... and {count - 5} more')
        else:
            self.stdout.write('No expired email verification codes found')
            
        return count