import os
import sys


# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from tibia_hunts.wsgi import application  # noqa: E402


# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This provides that for our Django WSGI application.
app = application
