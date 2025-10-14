from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]
    
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects", verbose_name="Team Members")
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing') 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects_updated_by')

    def __str__(self):
        return self.name
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    
    objects = models.Manager()

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_deleted=False)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
git add .gitignore
