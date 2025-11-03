from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Unified dashboard: team users manage their own records, admin sees read-only view
    path('dashboard/', views.customerdetailed_dashboard, name='customerdetailed_dashboard'),

    # ✏️ Edit customer entry (only owner, not Azure admin)
    path('dashboard/edit/<int:pk>/', views.edit_customer, name='edit_customer'),

    # 🗑️ Delete customer entry (only owner, not Azure admin)
    path('dashboard/delete/<int:pk>/', views.delete_customer, name='delete_customer'),
]


