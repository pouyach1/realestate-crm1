from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'status', 'created_at']
    list_filter = ['property_type', 'status']
    search_fields = ['title', 'address']
    inlines = [PropertyImageInline]