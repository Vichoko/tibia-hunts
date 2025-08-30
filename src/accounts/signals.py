"""
Django signals for automatic profile management.

This module defines signal handlers that automatically create user profiles
when new users are created, ensuring data consistency between User and Profile models.
"""

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()
"""Django User model instance."""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a new User is created.

    This signal handler ensures that every User has an associated Profile,
    maintaining the one-to-one relationship between User and Profile models.

    Args:
        sender: The model class that sent the signal (User).
        instance: The actual instance being saved.
        created (bool): True if a new record was created.
        **kwargs: Additional keyword arguments from the signal.
    """
    if created:
        Profile.objects.create(user=instance)
