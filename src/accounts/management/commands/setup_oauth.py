import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Configure Google OAuth credentials in the database'

    def handle(self, *args, **options):
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
