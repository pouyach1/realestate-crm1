import django_filters
from django import forms
from django.db import models
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or address...'
        })
    )
    
    property_type = django_filters.ChoiceFilter(
        choices=Property.PROPERTY_TYPES,
        empty_label='All Types',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = django_filters.ChoiceFilter(
        choices=Property.STATUS_CHOICES,
        empty_label='All Status',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Min Price',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min $'})
    )
    
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Max Price',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max $'})
    )
    
    class Meta:
        model = Property
        fields = ['search', 'property_type', 'status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(address__icontains=value)
        )