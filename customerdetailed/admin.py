# A - Import Required Modules
from django.contrib import admin
from .models import Profile, CustomerDetailed

# B - Azure Admin Email
AZURE_ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Mixin: Restrict Admin Access to Azure Admin
class AzureAdminOnlyMixin:
    def has_module_permission(self, request):
        return request.user.is_active and request.user.email == AZURE_ADMIN_EMAIL

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.email == AZURE_ADMIN_EMAIL

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and request.user.email == AZURE_ADMIN_EMAIL

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active and request.user.email == AZURE_ADMIN_EMAIL

    def has_add_permission(self, request):
        return request.user.is_active and request.user.email == AZURE_ADMIN_EMAIL

# D - Profile Admin
@admin.register(Profile)
class ProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'created_at']
    list_filter = ['role', 'department']
    search_fields = ['user__username', 'user__email']

# E - CustomerDetailed Admin
@admin.register(CustomerDetailed)
class CustomerDetailedAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['name', 'company', 'created_by', 'team', 'status', 'created_at']
    list_filter = ['team', 'status', 'created_by']
    search_fields = ['name', 'company', 'email', 'created_by__username']


