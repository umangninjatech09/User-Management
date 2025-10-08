from django.db import models
from django.conf import settings
# settings.AUTH_USER_MODEL resolves to 'management.User'

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    approved_status = models.CharField(max_length=10, choices=APPROVED_STATUS_CHOICES, default='Pending')
    is_deleted = models.BooleanField(default=False)
    
    # Using 'on_delete=models.SET_NULL' for integrity
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='leaves_created_by' # Changed related_name to avoid clash
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='leaves_updated_by' # Changed related_name to avoid clash
    )

    def __str__(self):
        # Accessing email from the User model for a clearer string representation
        return f"{self.user.email} - {self.leave_type} from {self.start_date} to {self.end_date}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    objects = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_deleted=False)
    
    class Meta:
        verbose_name = "Leave Request"
        verbose_name_plural = "Leave Requests"
