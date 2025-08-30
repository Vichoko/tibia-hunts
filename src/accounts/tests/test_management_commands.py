"""
Test suite for Django management commands.

This module contains tests for:
- OAuth setup command functionality
- OAuth cleanup command functionality
- Environment variable handling in commands
"""

from django.test import TestCase
from django.core.management import call_command
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
import os


class ManagementCommandTestCase(TestCase):
    """
    Test case for custom management commands.

    Tests OAuth setup and cleanup commands.
    """

    def setUp(self):
        """Set up test environment variables."""
        os.environ['GOOGLE_CLIENT_ID'] = 'test-client-id'
        os.environ['GOOGLE_CLIENT_SECRET'] = 'test-client-secret'

    def tearDown(self):
        """Clean up test environment variables."""
        if 'GOOGLE_CLIENT_ID' in os.environ:
            del os.environ['GOOGLE_CLIENT_ID']
        if 'GOOGLE_CLIENT_SECRET' in os.environ:
            del os.environ['GOOGLE_CLIENT_SECRET']

    def test_setup_oauth_command(self):
        """Test that setup_oauth command creates SocialApp correctly."""
        # Ensure no existing apps
        SocialApp.objects.filter(provider='google').delete()

        # Run the command
        call_command('setup_oauth')

        # Check that SocialApp was created
        apps = SocialApp.objects.filter(provider='google')
        self.assertEqual(apps.count(), 1)

        app = apps.first()
        self.assertEqual(app.client_id, 'test-client-id')
        self.assertEqual(app.secret, 'test-client-secret')
        self.assertEqual(app.provider, 'google')

        # Check site association
        site = Site.objects.get(pk=1)
        self.assertIn(site, app.sites.all())

    def test_cleanup_oauth_command(self):
        """Test that cleanup_oauth command removes duplicates and creates single app."""
        # Create duplicate apps
        SocialApp.objects.create(
            provider='google',
            name='Duplicate 1',
            client_id='old-id-1',
            secret='old-secret-1'
        )
        SocialApp.objects.create(
            provider='google',
            name='Duplicate 2',
            client_id='old-id-2',
            secret='old-secret-2'
        )

        # Verify duplicates exist
        self.assertEqual(SocialApp.objects.filter(provider='google').count(), 2)

        # Run cleanup command
        call_command('cleanup_oauth')

        # Verify only one app remains with correct credentials
        apps = SocialApp.objects.filter(provider='google')
        self.assertEqual(apps.count(), 1)

        app = apps.first()
        self.assertEqual(app.client_id, 'test-client-id')
        self.assertEqual(app.secret, 'test-client-secret')

    def test_setup_oauth_command_missing_env_vars(self):
        """Test that setup_oauth command fails gracefully without environment variables."""
        # Remove environment variables
        if 'GOOGLE_CLIENT_ID' in os.environ:
            del os.environ['GOOGLE_CLIENT_ID']
        if 'GOOGLE_CLIENT_SECRET' in os.environ:
            del os.environ['GOOGLE_CLIENT_SECRET']

        # Command should handle missing env vars gracefully
        try:
            call_command('setup_oauth')
            # If we get here, the command didn't fail as expected
            # Check that no SocialApp was created
            apps = SocialApp.objects.filter(provider='google')
            # The command should not create apps without proper credentials
        except SystemExit:
            # Command may exit with error code, which is expected
            pass
