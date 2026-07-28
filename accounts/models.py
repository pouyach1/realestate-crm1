from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended profile for real estate agents"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    agency_name = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"