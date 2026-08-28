from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
        )

    def clean(self):
        """Custom validation to ensure that if the user is a superuser, they must also be staff."""
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")
        is_staff = cleaned_data.get("is_staff")

        if is_superuser and not is_staff:
            self.add_error("is_staff", "Superusers must also be staff.")

        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    """Form for updating an existing user."""

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
        )

    def clean(self):
        """Custom validation to ensure that if the user is a superuser, they must also be staff."""
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")
        is_staff = cleaned_data.get("is_staff")

        if is_superuser and not is_staff:
            self.add_error("is_staff", "Superusers must also be staff.")

        return cleaned_data
