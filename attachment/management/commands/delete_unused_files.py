from django.core.management.base import BaseCommand
from django.utils import timezone
from attachment.models import MFile
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete unused AFile objects that are older than 10 minutes.'

    def handle(self, *args, **kwargs):
        # Calculate the time 10 minutes ago
        time_threshold = timezone.now() - timedelta(minutes=10)

        # Filter and delete unused AFile objects older than 10 minutes
        unused_files = MFile.objects.filter(state='0', sent_at__lt=time_threshold)
        count, _ = unused_files.delete()

        # Output the result to the console
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} unused files.'))
