# TibiaHunts — Current Architecture (MVP)

> Objective: Simple MVP deployed on Google App Engine using Django and SQLite — staying in **$0/month** using generous free tiers.

---

## 1) High‑Level Overview

**Principles**: Minimal complexity, scale‑to‑zero, single service deployment, cost‑efficient.

**Current Stack**

* **Frontend + Backend**: Google App Engine **Standard** (Python 3.11) with Django framework
* **Database**: SQLite (local file database)
* **Static Files**: Served directly through App Engine with 1-hour caching
* **Deployment**: Single `app.yaml` configuration with cost optimization settings

**Why this is cost-effective**

* Single App Engine Standard instance (F1-class equivalent) 
* Scale to zero when no traffic (`min_instances: 0`)
* SQLite requires no external database costs
* Static file caching reduces requests
* Simple architecture = minimal moving parts

---

## 2) Current Architecture Diagram (ASCII)

```
[ Browser ]
    |  HTTPS
    v
[ App Engine Standard (Python 3.11) ]
    |
    v
[ Django Application ]
    |
    v
[ SQLite Database (local file) ]

[ Static Files ] --> [ App Engine Static Handler ] --> [ 1h Cache ]
```

---

## 3) Current Implementation Details

### 3.1 App Engine Configuration

**Current `app.yaml` settings:**

* **Runtime**: Python 3.11
* **Scaling**: 
  - `min_instances: 0` (scale to zero)
  - `max_instances: 1` (cost control)
  - `target_cpu_utilization: 0.8`
  - `max_concurrent_requests: 80`
* **Resources**: 1 CPU, 0.5GB memory, 10GB disk
* **Static Files**: `/static` with 1-hour expiration

### 3.2 Django Application

* **Framework**: Django 5.2
* **Settings**: Environment-based configuration (`local.py`, `cloud.py`)
* **Security**: Production settings with secure headers when deployed
* **Database**: SQLite with local `db.sqlite3` file

### 3.3 Database (SQLite)

* **Type**: File-based SQLite database
* **Location**: `src/db.sqlite3`
* **Benefits**: 
  - Zero external database costs
  - Simple deployment (included in app)
  - Sufficient for MVP traffic levels
* **Limitations**: 
  - Single-instance only (App Engine Standard handles this)
  - Limited concurrent writes (acceptable for MVP)

### 3.4 Deployment

* **Process**: Direct deployment to App Engine using `gcloud app deploy`
* **Environment Variables**: Set in `app.yaml` for production
* **Static Files**: Handled by App Engine's built-in static file serving

---

## 4) Cost Optimization Features

### 4.1 App Engine Optimizations

* **Scale to Zero**: No costs when no traffic
* **Single Instance Limit**: Prevents unexpected scaling costs
* **Resource Limits**: Minimum viable memory and disk allocation
* **Efficient Static Serving**: Reduces dynamic request load

### 4.2 Database Optimizations

* **SQLite**: No external database costs
* **Local Storage**: Included in App Engine instance

---

## 5) Future Considerations

When the application grows beyond MVP stage, consider:

* **Database**: Migrate to Cloud SQL or Firestore for better scalability
* **Authentication**: Add Firebase Auth or Django's built-in auth
* **File Storage**: Cloud Storage for user uploads
* **Caching**: Redis/Memcache for better performance
* **Monitoring**: Enhanced logging and error reporting

---

## 6) Current Limitations

* **Single Instance**: SQLite limits us to one instance (acceptable for MVP)
* **No Authentication**: Currently no user system implemented
* **No File Uploads**: No external storage configured
* **Basic Monitoring**: Relies on App Engine's default logging

This architecture prioritizes simplicity and cost-effectiveness for the MVP phase while maintaining a clear upgrade path for future features.
