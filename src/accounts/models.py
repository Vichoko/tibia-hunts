"""
User profile models for the accounts app.

This module defines the Profile model that extends Django's built-in User model
with additional user information and customization options for TibiaHunts users.
"""

from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Extended user profile model.

    Provides additional user information beyond Django's default User model,
    including display name and avatar URL for social authentication integration.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """One-to-one relationship with Django's User model."""

    display_name = models.CharField(max_length=120, blank=True)
    """User's preferred display name, can be different from username."""

    avatar_url = models.URLField(blank=True)
    """URL to user's profile picture from social authentication providers."""

    created_at = models.DateTimeField(auto_now_add=True)
    """Timestamp when the profile was created."""

    def __str__(self):
        """
        Return string representation of the profile.

        Returns:
            str: Display name if available, otherwise username.
        """
        return self.display_name or self.user.get_username()
