"""
Cloud settings for tibia_hunts project (Google App Engine).
"""

import os
import logging
from .common import *

# Print which settings module is being used
logger = logging.getLogger(__name__)
logger.info("🌍 Using CLOUD settings (Google App Engine)")

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = ['*']  # GAE handles the host filtering

# Security enhancements
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files configuration for cloud
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
