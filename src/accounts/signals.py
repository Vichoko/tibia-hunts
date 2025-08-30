"""
Django signals for automatic profile management.

This module defines signal handlers that automatically create user profiles
when new users are created, ensuring data consistency between User and Profile models.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


User = get_user_model()
"""Django User model instance."""


@receiver(post_save, sender=User)
def create_profile(_sender, instance, created, **_kwargs):
    """
    Automatically create a Profile when a new User is created.

    This signal handler ensures that every User has an associated Profile,
    maintaining the one-to-one relationship between User and Profile models.

    Args:
        _sender: The model class that sent the signal (User) - unused.
        instance: The actual instance being saved.
        created (bool): True if a new record was created.
        **_kwargs: Additional keyword arguments from the signal - unused.
    """
    if created:
        Profile.objects.create(user=instance)
