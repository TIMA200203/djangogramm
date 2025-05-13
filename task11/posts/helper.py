from django.core.exceptions import ValidationError
from PIL import Image
import hashlib
import os
from unidecode import unidecode


def get_upload_path(instance, filename):  
    ext = filename.split('.')[-1]

    try:
        Image.open(instance.image)
    except IOError:
        raise ValidationError(('Uploaded file is not an image.'))

    filename = f"{hashlib.md5(os.urandom(64)).hexdigest()}.{ext}"
    filename = unidecode(filename)
    return os.path.join('post_images', filename)
