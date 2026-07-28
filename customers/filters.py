import django_filters
from django import forms
from django.db import models
from .models import Customer


class CustomerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, phone, or email...'
        })
    )
    
    request_type = django_filters.ChoiceFilter(
        choices=Customer.REQUEST_TYPE_CHOICES,
        empty_label='All Types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Customer
        fields = ['search', 'request_type']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(phone__icontains=value) |
            models.Q(email__icontains=value)
        )