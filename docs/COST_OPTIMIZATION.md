# Cost Optimization Guide for Google App Engine

## Overview
This guide helps keep your Django app within a $10 USD/month budget on Google App Engine.

## Current Optimizations Applied

### 1. App Engine Configuration (`app.yaml`)
- **Scale to Zero**: `min_instances: 0` - App shuts down when no traffic
- **Single Instance Max**: `max_instances: 1` - Prevents multiple instances
- **Minimal Resources**: 0.5GB RAM, 1 CPU, 10GB disk
- **High CPU Threshold**: 80% before scaling (vs default 60%)
- **Static File Caching**: 1-hour cache to reduce requests

### 2. Dependencies Optimization
- ❌ Removed `psycopg2-binary` (not needed with SQLite)
- ❌ Removed `google-cloud-storage` (using local static files)
- ✅ Kept only essential: `django`, `gunicorn`
- **Result**: Reduced from ~25 packages to ~7 packages

### 3. Database Strategy
- **SQLite**: Free, no Cloud SQL costs
- **Local Storage**: Database file stored with app instance
- **Note**: Data persists during app lifetime but may be lost on restarts

### 4. Performance Optimizations
- **Local Memory Cache**: No external cache service costs
- **Optimized Sessions**: Cached database sessions
- **Minimal Logging**: Only warnings/errors to reduce log storage

## Expected Monthly Costs (Estimates)

### Free Tier Allowances (Always Free)
- 28 instance hours per day
- 1GB outbound data per day
- 5GB Cloud Storage

### Paid Usage (if exceeded)
- **Instance Hours**: $0.05/hour after free tier
- **Outbound Bandwidth**: $0.12/GB after 1GB/day
- **Storage**: ~$0.026/GB/month for SQLite file

### Realistic Usage Scenarios

#### Low Traffic (< 100 visits/day)
- **Cost**: $0-2/month
- **Stays within free tier most days**

#### Medium Traffic (500-1000 visits/day)
- **Cost**: $3-7/month
- **Some paid instance hours**

#### High Traffic (2000+ visits/day)
- **Cost**: $8-15/month
- **May exceed $10 budget**

## Additional Cost-Saving Strategies

### 1. Enable Further Optimizations
```yaml
# Add to app.yaml for even more savings
automatic_scaling:
  min_instances: 0
  max_instances: 1
  target_cpu_utilization: 0.9  # Even higher threshold
  min_pending_latency: 30ms    # Wait longer before scaling
  max_pending_latency: automatic
```

### 2. Monitor Usage
```bash
# Check your current usage
gcloud app instances list
gcloud logging read "resource.type=gae_app" --limit=10
```

### 3. Set Budget Alerts
- Go to Google Cloud Console → Billing → Budgets
- Set alert at $8 (80% of $10 budget)
- Set another alert at $10 (100% of budget)

### 4. Alternative Architecture for Ultra-Low Cost
If costs exceed budget, consider:
- **Static Site + API**: Use GitHub Pages + minimal App Engine API
- **Scheduled Scaling**: Use Cloud Scheduler to stop/start app
- **Serverless Functions**: Use Cloud Functions for specific features

## Monitoring Commands

```bash
# Check current costs
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID

# Monitor app performance
gcloud app logs tail -s default
gcloud app instances list

# Check quotas
gcloud app quotas list
```

## When to Consider Upgrades

Only when you have sustainable revenue:
1. **Cloud SQL**: When you need persistent, reliable database
2. **Cloud Storage**: When you need file uploads
3. **Multiple Instances**: When single instance can't handle load
4. **Redis Cache**: When you need shared cache across instances

## Emergency Cost Control

If costs spike:
```bash
# Immediately stop all traffic
gcloud app versions stop VERSION_ID

# Or delete the app entirely
gcloud app services delete default --version=VERSION_ID
```

Remember: With current setup, your app should comfortably stay under $10/month for moderate traffic!
