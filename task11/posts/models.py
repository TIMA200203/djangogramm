from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.db import models
from .helper import get_upload_path
from PIL import Image
from cloudinary.models import CloudinaryField

class Post_in_site(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    text_for_post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(get_user_model(), related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Пост для {self.user.username} в {self.created_at}"

    def total_likes(self):
        return self.likes.count()


class PostImage(models.Model):
    post = models.ForeignKey(Post_in_site, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')

    def __str__(self):
        return f"Картинка для ID {self.post.id}"

class Tag_For_Pots(models.Model):
    name = models.CharField(max_length=50, unique=True)
    posts = models.ManyToManyField(Post_in_site, related_name='tags')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image.path)

            if img.width > 800 or img.height > 800:
                new_size = (800, 800)
                img.thumbnail(new_size)

            img.save(self.image.path, optimize=True, quality=85)

        super().save(*args, **kwargs)
