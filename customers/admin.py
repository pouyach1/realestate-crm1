from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'request_type', 'created_at']
    list_filter = ['request_type', 'created_at']
    search_fields = ['name', 'phone', 'email']
    date_hierarchy = 'created_at'