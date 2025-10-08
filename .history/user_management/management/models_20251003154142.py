from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.username

from django.db import models

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name
