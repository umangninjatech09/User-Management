from django.contrib import admin
from app.project.models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'start_date', 'end_date', 'status')
    search_fields = ('name', 'description', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('id',)
