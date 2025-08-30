# Google OAuth Credentials Update Script
# Run this after creating OAuth credentials in Google Cloud Console

param(
    [Parameter(Mandatory=$true)]
    [string]$ClientId,

    [Parameter(Mandatory=$true)]
    [string]$ClientSecret
)

Write-Host "Updating .env with Google OAuth credentials..." -ForegroundColor Green

# Backup existing .env
if (Test-Path ".env") {
    Copy-Item ".env" ".env.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Created backup of existing .env file" -ForegroundColor Yellow
}

# Update .env file with escaped characters
$envContent = @"
# Google OAuth Configuration - REAL CREDENTIALS
GOOGLE_CLIENT_ID=$ClientId
GOOGLE_CLIENT_SECRET=$ClientSecret

# Django Configuration
SECRET_KEY=django-insecure-local-dev-key-r48^0v53p6ue9-uy-47yc3a8x4f-h5-m-at-g-1a8pqfn-w2
DEBUG=True
"@

$envContent | Out-File -FilePath ".env" -Encoding utf8
Write-Host "Updated .env with real Google OAuth credentials" -ForegroundColor Green

Write-Host ""
Write-Host "Ready to test! Run:" -ForegroundColor Cyan
Write-Host "   cd src" -ForegroundColor White
Write-Host "   python manage.py runserver 8000" -ForegroundColor White
Write-Host ""
Write-Host "Then visit: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "Test OAuth: Click 'Sign in with Google'" -ForegroundColor Cyan
Write-Host "Test API: http://localhost:8000/api/me" -ForegroundColor Cyan
