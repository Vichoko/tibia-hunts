# Google OAuth Credentials Update Script
# Run this after creating OAuth credentials in Google Cloud Console

<#
.SYNOPSIS
    Updates the .env file with Google OAuth credentials for TibiaHunts development.

.DESCRIPTION
    This PowerShell script automates the process of configuring Google OAuth credentials
    in the .env file for local TibiaHunts development. It safely backs up existing
    configurations and updates environment variables with real Google OAuth credentials.

.PARAMETER ClientId
    The Google OAuth Client ID from Google Cloud Console.
    Format: your-client-id.apps.googleusercontent.com

.PARAMETER ClientSecret
    The Google OAuth Client Secret from Google Cloud Console.
    Format: GOCSPX-xxxxxxxxxxxxxxxxxxxxx

.EXAMPLE
    .\scripts\update-env-credentials.ps1 -ClientId "123456-abcdef.apps.googleusercontent.com" -ClientSecret "GOCSPX-abcdef123456"

    Updates the .env file with the provided Google OAuth credentials.

.EXAMPLE
    $clientId = "123456789-abcdefghijklmnop.apps.googleusercontent.com"
    $secret = "GOCSPX-YourSecretKeyHere123456"
    .\scripts\update-env-credentials.ps1 -ClientId $clientId -ClientSecret $secret

    Using variables to store credentials before updating .env file.

.NOTES
    File Name      : update-env-credentials.ps1
    Author         : TibiaHunts Development Team
    Prerequisite   : PowerShell 5.0+
    Created        : 2025-08-30

    CONTEXTS OF USE:

    1. INITIAL SETUP (First time developers):
       - After cloning the repository
       - After creating Google OAuth credentials in Google Cloud Console
       - Before running the Django development server for the first time

    2. CREDENTIAL ROTATION:
       - When Google OAuth credentials expire or are compromised
       - When switching between different Google Cloud projects
       - When updating from development to staging credentials

    3. TEAM ONBOARDING:
       - New developers joining the project
       - Setting up development environments on new machines
       - Sharing credentials securely within the development team

    4. CI/CD INTEGRATION:
       - Local testing before pushing to remote repositories
       - Validating OAuth integration in development environment
       - Setting up test credentials for local integration tests

    PREREQUISITES:
    - Google Cloud Console project created
    - OAuth 2.0 Client ID created with correct redirect URI
    - Redirect URI configured as: http://localhost:8000/accounts/google/login/callback/
    - PowerShell execution policy allows script execution

    SECURITY CONSIDERATIONS:
    - This script creates backups of existing .env files with timestamps
    - Never commit the .env file to version control (.gitignore protects it)
    - Store credentials securely and rotate them regularly
    - Use different credentials for development, staging, and production

    POST-EXECUTION STEPS:
    1. Run: cd src && python manage.py runserver 8000
    2. Test OAuth: http://localhost:8000/ -> "Sign in with Google"
    3. Verify API: http://localhost:8000/api/me
    4. Check Django admin if needed: http://localhost:8000/admin/

.LINK
    https://console.cloud.google.com/apis/credentials

.LINK
    https://github.com/Vichoko/tibia-hunts/blob/main/README.md#quick-start-google-login-local
#>

param(
    [Parameter(Mandatory=$true, HelpMessage="Google OAuth Client ID from Google Cloud Console")]
    [ValidatePattern(".*\.apps\.googleusercontent\.com$")]
    [string]$ClientId,

    [Parameter(Mandatory=$true, HelpMessage="Google OAuth Client Secret from Google Cloud Console")]
    [ValidatePattern("^GOCSPX-.*")]
    [string]$ClientSecret
)

# Script configuration
$ErrorActionPreference = "Stop"
$envFile = ".env"
$backupTimestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupFile = ".env.backup.$backupTimestamp"

Write-Host "🔧 TibiaHunts OAuth Credentials Update Script" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Validate we're in the correct directory
if (-not (Test-Path "pyproject.toml") -or -not (Test-Path "src/manage.py")) {
    Write-Host "❌ ERROR: Script must be run from the TibiaHunts project root directory" -ForegroundColor Red
    Write-Host "   Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "   Expected files: pyproject.toml, src/manage.py" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Project root directory validated" -ForegroundColor Green

# Backup existing .env file if it exists
if (Test-Path $envFile) {
    try {
        Copy-Item $envFile $backupFile -ErrorAction Stop
        Write-Host "📦 Created backup: $backupFile" -ForegroundColor Yellow
    }
    catch {
        Write-Host "❌ ERROR: Failed to create backup of existing .env file" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "📝 No existing .env file found, creating new one" -ForegroundColor Yellow
}

# Validate credentials format
Write-Host "🔍 Validating credential formats..." -ForegroundColor Cyan

if ($ClientId -notmatch "^\d+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com$") {
    Write-Host "❌ ERROR: Invalid Client ID format" -ForegroundColor Red
    Write-Host "   Expected: numbers-alphanumeric.apps.googleusercontent.com" -ForegroundColor Yellow
    Write-Host "   Received: $ClientId" -ForegroundColor Yellow
    exit 1
}

if ($ClientSecret -notmatch "^GOCSPX-[a-zA-Z0-9_-]+$") {
    Write-Host "❌ ERROR: Invalid Client Secret format" -ForegroundColor Red
    Write-Host "   Expected: GOCSPX-alphanumeric" -ForegroundColor Yellow
    Write-Host "   Received: $($ClientSecret.Substring(0, 10))..." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Credential formats validated" -ForegroundColor Green

# Create the .env content
$envContent = @"
# Google OAuth Configuration - REAL CREDENTIALS
# Generated by update-env-credentials.ps1 on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
GOOGLE_CLIENT_ID=$ClientId
GOOGLE_CLIENT_SECRET=$ClientSecret

# Django Configuration
SECRET_KEY=django-insecure-local-dev-key-r48^0v53p6ue9-uy-47yc3a8x4f-h5-m-at-g-1a8pqfn-w2
DEBUG=True

# Development Settings
# Add additional environment variables here as needed
"@

# Write the .env file
try {
    $envContent | Out-File -FilePath $envFile -Encoding utf8 -ErrorAction Stop
    Write-Host "✅ Successfully updated $envFile with Google OAuth credentials" -ForegroundColor Green
}
catch {
    Write-Host "❌ ERROR: Failed to write .env file" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Display success information
Write-Host ""
Write-Host "🎉 Configuration completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. cd src" -ForegroundColor White
Write-Host "   2. python manage.py runserver 8000" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Test URLs:" -ForegroundColor Cyan
Write-Host "   • Home: http://localhost:8000/" -ForegroundColor White
Write-Host "   • OAuth: Click 'Sign in with Google'" -ForegroundColor White
Write-Host "   • API: http://localhost:8000/api/me" -ForegroundColor White
Write-Host "   • Admin: http://localhost:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "🔒 Security Notes:" -ForegroundColor Yellow
Write-Host "   • .env file is protected by .gitignore" -ForegroundColor White
Write-Host "   • Backup created: $backupFile" -ForegroundColor White
Write-Host "   • Never commit .env to version control" -ForegroundColor White
Write-Host ""
Write-Host "💡 Troubleshooting:" -ForegroundColor Magenta
Write-Host "   • If OAuth fails, check redirect URI in Google Console" -ForegroundColor White
Write-Host "   • Ensure redirect URI: http://localhost:8000/accounts/google/login/callback/" -ForegroundColor White
Write-Host "   • Run: python manage.py cleanup_oauth if issues persist" -ForegroundColor White
