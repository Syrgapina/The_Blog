from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    about_me = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True)



