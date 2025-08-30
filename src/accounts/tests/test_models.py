"""
Test suite for Profile model functionality.

This module contains tests for:
- Profile model methods and string representation
- Profile field validation and properties
- Profile-User relationship functionality
"""

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Profile


class ProfileModelTestCase(TestCase):
    """
    Test case for the Profile model functionality.

    Tests model methods, string representation, and field validation.
    """

    def setUp(self):
        """Set up test user and profile."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com"
        )

    def test_profile_str_with_display_name(self):
        """Test Profile __str__ method returns display_name when available."""
        profile = self.user.profile
        profile.display_name = "Custom Display Name"
        profile.save()

        assert str(profile) == "Custom Display Name"

    def test_profile_str_without_display_name(self):
        """Test Profile __str__ method returns username when display_name is empty."""
        profile = self.user.profile
        profile.display_name = ""
        profile.save()

        assert str(profile) == "testuser"

    def test_profile_fields(self):
        """Test Profile model fields and their properties."""
        profile = self.user.profile
        profile.display_name = "Test Display Name"
        profile.avatar_url = "https://example.com/avatar.jpg"
        profile.save()

        # Reload from database
        profile.refresh_from_db()

        assert profile.display_name == "Test Display Name"
        assert profile.avatar_url == "https://example.com/avatar.jpg"
        assert profile.created_at is not None
        assert profile.user == self.user

    def test_profile_creation_signal(self):
        """Test that Profile is automatically created via signals."""
        # Create a new user
        new_user = User.objects.create_user(
            username="newuser", email="newuser@example.com"
        )

        # Verify profile was created automatically
        assert hasattr(new_user, "profile")
        assert isinstance(new_user.profile, Profile)

    def test_profile_one_to_one_relationship(self):
        """Test the one-to-one relationship between User and Profile."""
        profile = self.user.profile

        # Test reverse relationship
        assert profile.user == self.user

        # Test that profile is unique per user
        profile_count = Profile.objects.filter(user=self.user).count()
        assert profile_count == 1
