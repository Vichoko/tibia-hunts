# Deployment script for Google App Engine (Windows PowerShell)

Write-Host "🚀 Starting deployment to Google App Engine..." -ForegroundColor Green

# Check if gcloud is installed
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Google Cloud SDK not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Update requirements.txt from poetry
Write-Host "📦 Updating requirements.txt..." -ForegroundColor Yellow
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Collect static files
Write-Host "🎨 Collecting static files..." -ForegroundColor Yellow
poetry run python src/manage.py collectstatic --noinput

# Run Django checks
Write-Host "🔍 Running Django checks..." -ForegroundColor Yellow
poetry run python src/manage.py check --deploy

# Deploy to App Engine
Write-Host "☁️ Deploying to Google App Engine..." -ForegroundColor Blue
gcloud app deploy --quiet

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Your app should be available at: https://YOUR-PROJECT-ID.appspot.com" -ForegroundColor Cyan
