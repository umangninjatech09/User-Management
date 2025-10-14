from django.contrib import admin
from app.leaves.models import Leaves 

@admin.register(Leaves)
class LeaveAdmin(admin.ModelAdmin):
    # FIX: Change 'status' to 'approved_status'
    list_display = ('id', 'user', 'start_date', 'end_date', 'approved_status') 
    ordering = ('id',)
    
    # FIX: Change 'status' to 'approved_status' for searching
    search_fields = ('user__username', 'approved_status')