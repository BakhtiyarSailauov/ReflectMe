from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Notation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notations')
    tag_notion = models.TextField(max_length=100, default='default_value')
    topic_notion = models.TextField(max_length=100, default='default_value')
    content = models.TextField(max_length=100, default='default_value')
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.topic_notion


class Friendship(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friends_with")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username