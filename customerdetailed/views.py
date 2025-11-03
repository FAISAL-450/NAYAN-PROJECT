# A - Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import PermissionDenied

from .models import CustomerDetailed
from .forms import CustomerDetailedForm

# B - Access Control Configuration
ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'
TEAM_EMAILS = [
    'kash@dzignscapeprofessionals.onmicrosoft.com',
    'bappi@dzignscapeprofessionals.onmicrosoft.com',
]

# C - Access Control Helpers
def is_admin_user(user):
    return user.email == ADMIN_EMAIL

def is_team_user(user):
    return user.email in TEAM_EMAILS

# D - Query Filtering Logic
def filter_customerdetaileds(query=None, user=None):
    queryset = CustomerDetailed.objects.all()

    if is_admin_user(user):
        queryset = queryset.exclude(created_by=user)  # Admin sees others' data
    elif is_team_user(user):
        queryset = queryset.filter(created_by=user)   # Team sees own data
    else:
        queryset = queryset.none()  # No access

    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    return queryset

# E - Pagination Helper
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# F - Dashboard View (Team + Admin)
@login_required
def customerdetailed_dashboard(request):
    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None)

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    # ✅ Only team users can submit
    if is_team_user(request.user) and request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.created_by = request.user
        customer.team = getattr(request.user.customerdetailed_profile, "role", "support")
        customer.save()
        messages.success(request, "✅ Customer record created successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    return render(request, "customerdetailed/customerdetailed_dashboard.html", {
        "customerdetaileds": customerdetaileds_page,
        "query": query,
        "form": form,
        "mode": "list",
        "readonly": is_admin_user(request.user)
    })

# G - Edit View (Team Only, Own Records)
@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if not is_team_user(request.user) or customer.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()
    form = CustomerDetailedForm(request.POST or None, instance=customer)

    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Customer record updated successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    customerdetaileds = filter_customerdetaileds(query=query, user=request.user)
    customerdetaileds_page = get_paginated_queryset(request, customerdetaileds)

    return render(request, "customerdetailed/customerdetailed_dashboard.html", {
        "form": form,
        "mode": "edit",
        "customer": customer,
        "query": query,
        "customerdetaileds": customerdetaileds_page,
        "readonly": False
    })

# H - Delete View (Team Only, Own Records)
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(CustomerDetailed, pk=pk)

    if not is_team_user(request.user) or customer.created_by != request.user:
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f"🗑️ Customer '{name}' deleted successfully.")
        return redirect(f"{reverse('customerdetailed_dashboard')}?q={query}")

    return render(request, "customerdetailed/confirm_delete.html", {
        "customer": customer,
        "query": query
    })



