from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


class NewPost(models.Model):
    # id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    no_of_likes = models.IntegerField(default=0)


class PostComment(models.Model):
    post = models.ForeignKey('NewPost', related_name="post_comments", null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)