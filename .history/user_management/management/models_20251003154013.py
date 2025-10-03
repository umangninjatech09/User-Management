from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.username

class 