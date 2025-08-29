#!/bin/bash

# Deployment script for Google App Engine

echo "🚀 Starting deployment to Google App Engine..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Update requirements.txt from poetry
echo "📦 Updating requirements.txt..."
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Collect static files
echo "🎨 Collecting static files..."
poetry run python src/manage.py collectstatic --noinput --settings=tibia_hunts.settings_production

# Run Django checks
echo "🔍 Running Django checks..."
poetry run python src/manage.py check --deploy --settings=tibia_hunts.settings_production

# Deploy to App Engine
echo "☁️ Deploying to Google App Engine..."
gcloud app deploy --quiet

echo "✅ Deployment completed!"
echo "🌐 Your app should be available at: https://YOUR-PROJECT-ID.appspot.com"
