"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from project.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_client",
    )
    list_filter = ("is_client", "is_staff", "created", "modified")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ("user",)
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )


admin.site.register(User, CustomUserAdmin)
