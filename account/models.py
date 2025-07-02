from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from .util import getUserCode
from django.dispatch import receiver
from project.snowflake import getAccountAUserSnowflakeID
from hashlib import md5
import os
from UtilGlobal.validator.FieldFile import imagefile_validator
from media.models import MediaFileSystemStorage
from UtilGlobal.image.main import resize_image
from datetime import timedelta

# Create your models here.
    

class AUser(User):
    @staticmethod
    def md5_filename(n):
        s = os.path.splitext(n)
        return md5(s[0].encode('utf-8')).hexdigest() + s[1]

    def cover_dir_path(instance, filename):
        return f'usercover/{instance.urlCode}/' + AUser.md5_filename(filename)

    def avatar_dir_path(instance, filename):
        return f'avatar/{instance.urlCode}/' + AUser.md5_filename(filename)

    def scaled_avatar_dir_path(instance, filename):
        return f'avatar/{instance.urlCode}/scaled/' + AUser.md5_filename(filename)
    
    name = models.CharField(max_length=20,default='some_user')
    # username = models.CharField(  #只能包含_和数字 开头不能有数字或_ _不能2连 结尾不能_
    #     unique=True,
    #     null=False,
    #     blank=False,
    #     db_index=True,
    #     max_length=24,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^(?=.{6,20}$)(?![_0-9])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$',
    #             message='Enter a valid username',
    #             code='invalid_username'
    #         ),
    #     ]
    # )
    urlCode = models.PositiveBigIntegerField(default=getAccountAUserSnowflakeID, unique=True, db_index=True, primary_key=True)
    # sex = models.CharField(default='2',max_length = 2,choices = {('0', '男'),('1', '女'),('2', '0b01')})
    age = models.PositiveSmallIntegerField(default=None,blank=True,null=True)
    info = models.FileField(default=None,blank=True,null=True)
    additional = models.JSONField(default=dict, null=False)
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='', validators=[imagefile_validator], storage=MediaFileSystemStorage)
    avatar = models.ImageField(upload_to=avatar_dir_path, blank=True, default='',validators=[imagefile_validator], storage=MediaFileSystemStorage)
    scaled_avatar = models.ImageField(upload_to=scaled_avatar_dir_path, blank=True, default='',validators=[imagefile_validator], storage=MediaFileSystemStorage)

    def save(self, *args, **kwargs):
        isNew = self._state.adding
        if isNew:
            if self.avatar and not self.scaled_avatar:
                resized_image = resize_image(self.avatar, requested_size=200, as_file=True)  # Assume 200 is the target width for scaling
                
                # Set the resized image to scaled_avatar field
                self.scaled_avatar.save(self.avatar.name, resized_image, save=False)
        super().save(*args, **kwargs)
            

    def __str__(self) -> str:
        return f"{self.username}({self.urlCode})"
    
    class Meta:
        ordering = ['urlCode']


    

@receiver(models.signals.post_delete, sender=AUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

@receiver(models.signals.pre_save, sender=AUser)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `AUser` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        u = AUser.objects.get(pk=instance.pk)
        old_files = [u.avatar, u.cover]
    except AUser.DoesNotExist:
        return False

    if all([f == '' for f in old_files]):
        return
    new_files = [instance.avatar, instance.cover]
    
    for i in range(len(old_files)):
        old_file = old_files[i]
        new_file = new_files[i]
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)


class EmailVerificationCode(models.Model):
    """Model to store email verification codes"""
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    used_date = models.DateTimeField(null=True, blank=True)
    
    @property
    def is_expired(self):
        """Check if the verification code has expired (10 minutes)"""
        return timezone.now() > self.created_at + timedelta(minutes=10)
    
    @property
    def is_valid(self):
        """Check if the verification code is valid (not used and not expired)"""
        return not self.is_used and not self.is_expired
    
    @classmethod
    def create_code(cls, email, code):
        """Create a new verification code with timing restrictions"""
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        
        # Check for existing codes and enforce timing restrictions
        existing_codes = cls.objects.filter(email=email).order_by('-created_at')
        
        if existing_codes.exists():
            latest_code = existing_codes.first()
            
            if latest_code.is_used and latest_code.used_date:
                # If latest code was used, must wait 1 minute after use
                time_since_used = now - latest_code.used_date
                if time_since_used < timedelta(minutes=1):
                    remaining_seconds = 60 - time_since_used.total_seconds()
                    raise ValueError(f"请等待 {int(remaining_seconds)} 秒后再发送新验证码")
            elif not latest_code.is_used:
                # If latest code is unused, must wait 10 minutes after creation
                time_since_created = now - latest_code.created_at
                if time_since_created < timedelta(minutes=10):
                    remaining_seconds = 600 - time_since_created.total_seconds()
                    remaining_minutes = int(remaining_seconds / 60)
                    remaining_secs = int(remaining_seconds % 60)
                    raise ValueError(f"请等待 {remaining_minutes} 分 {remaining_secs} 秒后再发送新验证码")
        
        # Mark any existing unused codes as used (cleanup old codes)
        cls.objects.filter(email=email, is_used=False).update(is_used=True)
        
        # Create new code
        return cls.objects.create(email=email, code=code)
    
    @classmethod
    def verify_code(cls, email, code):
        """Verify a code and mark it as used if valid"""
        from django.utils import timezone
        
        try:
            verification = cls.objects.get(
                email=email, 
                code=code, 
                is_used=False
            )
            
            if verification.is_valid:
                verification.is_used = True
                verification.used_date = timezone.now()
                verification.save()
                return True
            return False
        except cls.DoesNotExist:
            return False
    
    def __str__(self):
        return f"{self.email} - {self.code}"
    
    class Meta:
        ordering = ['-created_at']
