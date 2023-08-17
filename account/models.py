from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer not to say'),
]
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    fb_social = models.URLField(blank=True, null=True)
    twitter_social = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    short_bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='media/profile_pictures/', blank=True)

    def __str__(self):
        return self.full_name


    
