"""
Django management command for configuring Google OAuth credentials.

This command sets up Google OAuth credentials in the django-allauth database,
creating the necessary SocialApp entries and site associations for proper
OAuth functionality.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    """
    Management command to configure Google OAuth credentials in the database.

    This command reads Google OAuth credentials from environment variables
    and creates the necessary SocialApp database entries for django-allauth
    to function properly with Google OAuth.
    """

    help = 'Configure Google OAuth credentials in the database'
    """Help text displayed when running python manage.py help setup_oauth."""

    def handle(self, *args, **options):
        """
        Execute the OAuth setup command.

        Reads GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET from environment
        variables and creates/updates the corresponding SocialApp entries
        in the database.

        Args:
            *args: Positional arguments passed to the command.
            **options: Keyword arguments passed to the command.
        """
        # Get credentials from environment variables
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables')
            )
            return

        # Get or create the default site
        site, created = Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'TibiaHunts Local'
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created site: {site.domain}')
            )

        # Create or update Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        if not created:
            # Update existing app with new credentials
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            self.stdout.write(
                self.style.SUCCESS('Updated existing Google OAuth app')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Created new Google OAuth app')
            )

        # Associate the app with the site
        google_app.sites.add(site)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully configured Google OAuth:\n'
                f'  Client ID: {client_id}\n'
                f'  Site: {site.domain}\n'
                f'  Provider: google'
            )
        )
