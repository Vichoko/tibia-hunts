import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Clean up duplicate Google OAuth apps and configure a single one'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables')
            )
            return

        # Delete all existing Google OAuth apps
        deleted_count = SocialApp.objects.filter(provider='google').delete()[0]
        if deleted_count > 0:
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing Google OAuth app(s)')
            )

        # Get or create the default site
        site, created = Site.objects.get_or_create(
            pk=1,
            defaults={
                'domain': 'localhost:8000',
                'name': 'TibiaHunts Local'
            }
        )

        # Update site to localhost:8000 if it exists
        if not created:
            site.domain = 'localhost:8000'
            site.name = 'TibiaHunts Local'
            site.save()

        self.stdout.write(
            self.style.SUCCESS(f'Site configured: {site.domain}')
        )

        # Create a single new Google social app
        google_app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )

        # Associate the app with the site
        google_app.sites.add(site)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully configured single Google OAuth app:\n'
                f'  Client ID: {client_id}\n'
                f'  Site: {site.domain}\n'
                f'  Provider: google\n'
                f'  App ID: {google_app.id}'
            )
        )
