from django.contrib import admin

from .models import Task  # Make sure to import your Task model

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completed', 'created_at')  # Customize fields as needed
    search_fields = ('title',)

admin.site.register(Task, TaskAdmin)