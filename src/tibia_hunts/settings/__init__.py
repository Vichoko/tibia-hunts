"""
Django settings for tibia_hunts project.

This module dynamically imports the appropriate settings based on the
DJANGO_SETTINGS_MODULE environment variable.

Supported values:
- 'local' (default): Local development settings
- 'cloud': Google App Engine production settings

Usage:
    export DJANGO_SETTINGS_MODULE=tibia_hunts.settings.cloud
    python manage.py runserver

Or in Windows:
    $env:DJANGO_SETTINGS_MODULE='tibia_hunts.settings.cloud'
    python manage.py runserver
"""

