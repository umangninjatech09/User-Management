from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
import random
import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [('M','Male'),('F','Female'),('O','Other')]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_used = models.BooleanField(default=False)
    last_token_issued_at = models.DateTimeField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='users_created_by')

    objects = UserManager()

    USERNAME_FIELD = "emai"
    REQUIRED_FIELDS = ["number"]  

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.otp_used = False
        self.save()
        return self.otp

    def verify_otp(self, otp):
        if not self.otp or self.otp != otp:
            return False
        if self.otp_used:
            return False
        if timezone.now() - self.otp_created_at > datetime.timedelta(minutes=5):
            return False

        self.otp_used = True
        self.save()
        return True
    

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()


# Models for Work Timing

class WorkTiming(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='worktimings_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='worktimings_updated_by')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    objects = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_deleted=False)