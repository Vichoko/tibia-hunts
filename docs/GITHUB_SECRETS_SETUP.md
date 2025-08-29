ent# GitHub Actions Secrets Setup for GCP Deployment

This document explains how to configure the GitHub secrets required for automatic deployment to Google App Engine.

## Required Secrets

### 1. DJANGO_SECRET_KEY
The Django secret key for production.

**Value:** `!5$v&5^vn4cplg5$siebf9laq&41s^gha!n^jq2e#ta6=x0tlu`

### 2. GCP_SA_KEY
Google Cloud Service Account key for authentication.

## Setting up GCP Service Account

### Step 1: Create Service Account
```bash
# Create service account
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions deployment" \
    --display-name="GitHub Actions"

# Get the service account email
export SA_EMAIL=github-actions@tibia-hunts-app.iam.gserviceaccount.com
```

### Step 2: Grant Required Permissions
```bash
# Grant App Engine Admin role
gcloud projects add-iam-policy-binding tibia-hunts-app \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/appengine.appAdmin"

# Grant Cloud Build Editor role
gcloud projects add-iam-policy-binding tibia-hunts-app \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/cloudbuild.builds.editor"

# Grant Storage Admin role (for app deployment)
gcloud projects add-iam-policy-binding tibia-hunts-app \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/storage.admin"

# Grant Service Account User role
gcloud projects add-iam-policy-binding tibia-hunts-app \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="roles/iam.serviceAccountUser"
```

### Step 3: Create and Download Key
```bash
# Create key file
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=${SA_EMAIL}

# The content of github-actions-key.json is what goes into GCP_SA_KEY secret
```

## Adding Secrets to GitHub

1. Go to your GitHub repository: https://github.com/Vichoko/tibia-hunts
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following repository secrets:

### DJANGO_SECRET_KEY
- Name: `DJANGO_SECRET_KEY`
- Value: `!5$v&5^vn4cplg5$siebf9laq&41s^gha!n^jq2e#ta6=x0tlu`

### GCP_SA_KEY
- Name: `GCP_SA_KEY`
- Value: Copy the entire content of `github-actions-key.json` file

## Environment Setup

The workflow also uses a GitHub Environment called `production` for additional security. To set this up:

1. Go to **Settings** → **Environments**
2. Create a new environment called `production`
3. Optionally, add protection rules (e.g., required reviewers)

## Testing the Workflow

After setting up the secrets:

1. Push any changes to the `main` branch
2. The workflow will automatically trigger
3. Monitor the deployment in the **Actions** tab
4. The app will be available at: https://tibia-hunts-app.uc.r.appspot.com

## Manual Deployment

You can also trigger deployment manually:

1. Go to **Actions** tab
2. Select "Deploy to Google App Engine" workflow
3. Click "Run workflow"
4. Select the branch and click "Run workflow"

## Cost Monitoring

Remember to monitor your GCP costs:
- Set up billing alerts at $8 and $10
- Check costs daily in Google Cloud Console
- The current configuration should stay under $10/month for moderate traffic

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Check service account permissions
2. **Quota Exceeded**: Monitor your free tier usage
3. **Build Failures**: Check the workflow logs in GitHub Actions

### Emergency Stop:
If costs spike unexpectedly:
```bash
gcloud app versions stop VERSION_ID
```
