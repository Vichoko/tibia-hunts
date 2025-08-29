# Google App Engine Deployment Guide

## Prerequisites

1. **Google Cloud Account**: Make sure you have a Google Cloud account with billing enabled
2. **Google Cloud SDK**: Install the Google Cloud SDK
   - Windows: Download from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - macOS: `brew install google-cloud-sdk`
   - Linux: Follow [official instructions](https://cloud.google.com/sdk/docs/install)

## Cost-Optimized Setup

This configuration is optimized to stay within a **$10 USD/month budget**. See [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) for detailed cost analysis.

### Key Cost Optimizations Applied:
- ✅ Scale to zero when no traffic
- ✅ Maximum 1 instance to control costs
- ✅ Minimal resource allocation (0.5GB RAM)
- ✅ SQLite database (no Cloud SQL costs)
- ✅ Local static files (no Cloud Storage costs)
- ✅ Reduced dependencies for faster deployments

## Setup Steps

### 1. Create a Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (replace PROJECT_ID with your desired project ID)
gcloud projects create YOUR-PROJECT-ID

# Set the project as default
gcloud config set project YOUR-PROJECT-ID

# Enable App Engine
gcloud app create --region=us-central1

# Set up billing alerts (IMPORTANT for cost control)
# Go to: Google Cloud Console → Billing → Budgets
# Create alert at $8 and $10
```

### 2. Configure Environment Variables

Edit the `app.yaml` file and update:
- `GOOGLE_CLOUD_PROJECT`: Your actual project ID
- `SECRET_KEY`: Generate a secure secret key for production

```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Deploy to App Engine

#### Using the deployment script (Recommended)

**Windows:**
```powershell
./deploy.ps1
```

**Linux/macOS:**
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Manual deployment

```bash
# Update requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Collect static files
poetry run python src/manage.py collectstatic --noinput --settings=tibia_hunts.settings_production

# Run checks
poetry run python src/manage.py check --deploy --settings=tibia_hunts.settings_production

# Deploy
gcloud app deploy
```

## Post-Deployment

1. Your app will be available at: `https://YOUR-PROJECT-ID.appspot.com`
2. You can view logs with: `gcloud app logs tail -s default`
3. To open the app in browser: `gcloud app browse`

## Cost Monitoring

### Essential Commands:
```bash
# Monitor costs
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID

# Check app status
gcloud app instances list

# View recent logs (minimal to reduce costs)
gcloud app logs read --limit=50
```

### Budget Management:
- **Expected cost**: $0-7/month for moderate traffic
- **Monitor daily**: Check Google Cloud Console billing
- **Emergency stop**: `gcloud app versions stop VERSION_ID`

## Database Considerations

**Current Setup**: SQLite (Cost: $0)
- ✅ Perfect for development and low-traffic apps
- ✅ No additional database costs
- ⚠️ Data may be lost on app restarts
- ⚠️ Not suitable for high-concurrent writes

**Future Upgrades** (when revenue justifies costs):
1. **Cloud SQL**: ~$7-15/month for small instance
2. **Firestore**: Pay-per-use NoSQL option
3. **Cloud Storage**: For file uploads (~$0.02/GB/month)

## Security Notes

- The current configuration uses environment variables for secrets
- Update `ALLOWED_HOSTS` in production settings to be more specific
- Current setup is secure for small applications
- Review all security settings in `settings_production.py`

## Performance Monitoring

- **App logs**: `gcloud app logs tail -s default`
- **Instance status**: `gcloud app instances list`
- **Performance**: Available in Google Cloud Console (free tier)
- **Uptime monitoring**: Set up in Cloud Monitoring

## Scaling Considerations

The current setup handles:
- **~1000 requests/day**: Comfortably within free tier
- **~10,000 requests/day**: May cost $2-5/month
- **>50,000 requests/day**: Consider architecture changes

For higher traffic, see cost optimization strategies in [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md).
