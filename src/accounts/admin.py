"""
Django admin configuration for the accounts app.

This module configures the Django admin interface for user account-related models,
providing an intuitive interface for managing user profiles and authentication data.
"""

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Profile model.

    Provides a comprehensive interface for managing user profiles with
    search capabilities and optimized display of profile information.
    """

    list_display = ("id", "user", "display_name", "created_at")
    """Display these fields in the admin list view."""

    search_fields = ("user__username", "user__email", "display_name")
    """Enable search functionality across these fields."""
