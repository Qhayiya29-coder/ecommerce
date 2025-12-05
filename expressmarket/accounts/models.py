from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    is_verified = models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)



    def __str__(self):
        return self.username
    
