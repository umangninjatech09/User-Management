from django.contrib import admin

# Register your models here.
from app.leaves.models import Leaves  # Assuming Leave is the model for leaves

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_date', 'end_date', 'status')  # Customize fields as needed
    search_fields = ('user__username', 'status')  # Customize search fields as needed