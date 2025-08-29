import os
from src.tibia_hunts.wsgi import application

# App Engine by default looks for a main.py file at the root of the app
# directory with a WSGI-compatible object called app.
# This provides that for our Django WSGI application.
app = application
