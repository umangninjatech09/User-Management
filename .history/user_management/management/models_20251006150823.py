from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
import random
import datetime


# ====================================================
# Custom User Manager
# ====================================================
class UserManager(BaseUserManager):
    def create_user(self, email, name, number, age, gender, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, number=number, age=age, gender=gender)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, number, age, gender, password=None):
        user = self.create_user(email, name, number, age, gender, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# ====================================================
# Custom User Model (Login with OTP)
# ====================================================
class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # OTP fields
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number', 'age', 'gender']

    def __str__(self):
        return f"{self.name} ({self.email})"

    # Generate random OTP
    def generate_otp(self):
        self.otp = f"{random.randint(100000, 999999)}"
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp

    # Verify OTP (valid for 5 minutes)
    def verify_otp(self, otp):
        if self.otp != otp:
            return False
        expiry_time = self.otp_created_at + datetime.timedelta(minutes=5)
        return timezone.now() <= expiry_time


# ====================================================
# Project Model
# ====================================================
class Project(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing')
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ['-created_at']


# ====================================================
# Leaves Model
# ====================================================
class Leaves(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Earned', 'Earned Leave'),
    ]

    APPROVED_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved_status = models.CharField(max_length=10, choices=APPROVED_STATUS_CHOICES, default='Pending')
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leaves_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leaves_updated'
    )

    def __str__(self):
        return f"{self.user.name} - {self.leave_type} ({self.start_date} to {self.end_date})"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ['-created_at']


# ====================================================
# WorkTiming Model
# ====================================================
class WorkTiming(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='work_timings')
    date = models.DateField()
    clock_in = models.TimeField()
    clock_out = models.TimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.date}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ['-date']
