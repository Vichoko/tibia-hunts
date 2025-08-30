"""
Test suite for authentication functionality and API endpoints.

This module contains tests for:
- User authentication API endpoints (/api/me)
- Home page rendering for different user states
- Google OAuth integration flow
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import Profile
import json


class AuthenticationTestCase(TestCase):
    """
    Test case for user authentication functionality.

    Tests API endpoints, profile creation, and view rendering
    for both authenticated and anonymous users.
    """

    def setUp(self):
        """Set up test client for HTTP requests."""
        self.client = Client()

    def test_home_page_shows_signin_for_anonymous_user(self):
        """Test that home page shows 'Sign in with Google' for anonymous users"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign in with Google')
        self.assertContains(response, '/accounts/google/login/')

    def test_api_me_returns_false_for_anonymous_user(self):
        """Test that /api/me returns authenticated: false for anonymous users"""
        response = self.client.get('/api/me')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = json.loads(response.content)
        self.assertEqual(data['authenticated'], False)
        self.assertIsNone(data['user'])

    def test_profile_auto_creation_on_user_creation(self):
        """Test that Profile is automatically created when User is created"""
        user = User.objects.create_user(username='testuser', email='test@example.com')

        # Profile should be created automatically via signals
        self.assertTrue(hasattr(user, 'profile'))
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)
        self.assertEqual(str(profile), 'testuser')  # display_name is empty, so returns username

    def test_api_me_returns_user_data_for_authenticated_user(self):
        """Test that /api/me returns user data for authenticated users"""
        user = User.objects.create_user(username='testuser', email='test@example.com')
        profile = user.profile
        profile.display_name = 'Test User'
        profile.avatar_url = 'https://example.com/avatar.jpg'
        profile.save()

        # Login the user
        self.client.force_login(user)

        response = self.client.get('/api/me')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['authenticated'], True)
        self.assertEqual(data['user']['id'], user.id)
        self.assertEqual(data['user']['email'], 'test@example.com')
        self.assertEqual(data['user']['display_name'], 'Test User')
        self.assertEqual(data['user']['avatar_url'], 'https://example.com/avatar.jpg')

    def test_home_page_shows_user_info_for_authenticated_user(self):
        """Test that home page shows user info and logout link for authenticated users"""
        user = User.objects.create_user(username='testuser', email='test@example.com')
        profile = user.profile
        profile.display_name = 'Test User'
        profile.save()

        # Login the user
        self.client.force_login(user)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re signed in as')
        self.assertContains(response, 'Test User')
        self.assertContains(response, '/accounts/logout/')
        self.assertContains(response, '/api/me')
        self.assertNotContains(response, 'Sign in with Google')
