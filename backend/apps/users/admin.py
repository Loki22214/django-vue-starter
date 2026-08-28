from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import reverse

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    readonly_fields = ["date_joined", "last_login"]
    ordering = ["email"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Meta", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    search_fields = ("email", "first_name", "last_name")

    def response_add(self, request, obj, post_url_continue=None):
        """Override the response_add method to redirect to the user list after adding a new user."""
        # If the user chose to add another user, continue with the default behavior
        if "_addanother" in request.POST:
            return super().response_add(request, obj, post_url_continue)
        # If the user chose to continue editing the same user, continue with the default behavior
        if "_continue" in request.POST:
            return super().response_add(request, obj, post_url_continue)

        return redirect(reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}_changelist"))
