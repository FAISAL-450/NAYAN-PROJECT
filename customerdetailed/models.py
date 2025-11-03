from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('analyst', 'Analyst'),
        ('support', 'Support'),
        ('executive', 'Executive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customerdetailed_profile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='support')
    department = models.CharField(max_length=50, blank=True)  # ✅ used by middleware
    created_at = models.DateTimeField(auto_now_add=True)      # ✅ audit trail

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class CustomerDetailed(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_customers')
    team = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # ✅ optional lifecycle tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ edit tracking

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Detail"
        verbose_name_plural = "Customer Details"




