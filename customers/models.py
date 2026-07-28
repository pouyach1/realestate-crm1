from django.db import models


class Customer(models.Model):
    """Customer model for real estate CRM"""
    
    REQUEST_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('sell', 'Sell'),
    ]
    
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    request_type = models.CharField(max_length=4, choices=REQUEST_TYPE_CHOICES, default='buy')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.name} - {self.get_request_type_display()}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('customers:detail', kwargs={'pk': self.pk})