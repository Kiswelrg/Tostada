from PIL import Image
import imghdr
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def is_image1(field_file):
    if not field_file:
        return False
    file_type = imghdr.what(field_file)
    return file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']


def imagefile_validator(field_file):
    if not field_file:
        return False,0
    try:
        img = Image.open(field_file)
        img.verify()  # Verify the file is an image
    except (IOError, SyntaxError):
        raise ValidationError(
            _("%(value)s is not an image"),
            params={"value": field_file.name},
        )
    
    if img.format not in ['JPEG', 'PNG', 'GIF', 'WebP']:
        raise ValidationError("Unsupported image format. Only JPEG/jpg, PNG, GIF, and WebP are allowed.")
    
