from django.contrib import admin
from app.management.models import User, WorkTiming

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'number', 'age', 'gender', 'otp', 'is_staff', 'is_active', 'is_deleted')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)

@admin.register(WorkTiming)
class WorkTimingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'clock_in', 'clock_out')
    search_fields = ('user__username', 'date')
    list_filter = ('date',)
    ordering = ('-date',)