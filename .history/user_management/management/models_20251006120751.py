from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.username



class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    objects = models.Manager()  
    active = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.active.filter(is_deleted=False)
    

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    
    objects = models.Manager()
    active = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.active.filter(is_deleted=False)
    


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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved_status = models.CharField(max_length=10, choices=APPROVED_STATUS_CHOICES, default='Pending')
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
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
        return f"{self.user.username} - {self.leave_type} from {self.start_date} to {self.end_date}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    objects = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_deleted=False)
    
