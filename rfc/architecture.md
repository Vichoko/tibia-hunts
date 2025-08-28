# TibiaHunts — Cost‑Optimized Architecture (MVP)

> Objective: ship a public MVP that lets players submit hunts, browse/search spots, and paste Tibia Hunt Analyzer exports — while staying in (or near) **\$0/month** using generous free tiers.

---

## 1) High‑Level Overview

**Principles**: one cloud (GCP), scale‑to‑zero, minimal moving parts, clear ceilings, and guardrails against bill surprises.

**Stack**

* **Frontend + API**: Google App Engine **Standard** (Node.js 20) — single service.
* **Auth**: Firebase Auth (email link + Google). Optional anonymous flow for quick submit.
* **Database**: Firestore **in Datastore mode** (document store) — free quotas fit MVP.
* **File storage**: GCS (default App Engine bucket) for Analyzer raw text and future images.
* **Job/cron**: App Engine Cron + Cloud Tasks (optional) for nightly spot aggregations.
* **Observability**: Cloud Logging (sampled), Error Reporting, basic uptime checks.
* **(Optional later)** CDN: Cloudflare in front for caching if needed.

**Why this is cheap**

* 1× F1 instance on App Engine Standard fits always‑free instance hours.
* Datastore free quotas (reads/writes/storage) cover early traffic.
* No cross‑cloud egress; single billing account + budget alerts.

---

## 2) Architecture Diagram (ASCII)

```
[ Browser ]
    |  HTTPS
    v
[ App Engine Standard (Node 20) ]  <---->  [ Firebase Auth ]
    |   ^                                   (token verify)
    |   |
    v   |
[ Firestore (Datastore mode) ]
    |
    v
[ GCS (default bucket) ]  <-- Analyzer raw text, images

[ App Engine Cron ] --> [ Aggregation tasks ] --> Firestore Spot aggregates
```

---

## 3) Services & Config

### 3.1 App Engine Standard (Node 20)

* **Scaling**: automatic, `instance_class: F1`, no min instances (allow cold starts), request timeouts ≤ 60s.
* **Env**: Node 20, TypeScript optional; serve SSR or classic server‑rendered pages.
* **Endpoints**: REST under `/api/v1/*`.
* **Rate‑limit**: in‑memory token bucket per IP (or Firestore counter) to protect free tiers.

**`app.yaml` (baseline)**

```yaml
runtime: nodejs20
instance_class: F1
automatic_scaling:
  min_idle_instances: 0
  max_instances: 1
  target_cpu_utilization: 0.7
handlers:
  - url: /api/.*
    script: auto
    secure: always
  - url: /(.*)
    static_files: public/\1
    upload: public/.*
    secure: always
env_variables:
  NODE_ENV: production
  FIRESTORE_PROJECT_ID: your-project-id
  FIREBASE_WEB_CLIENT_ID: your-client-id
```

### 3.2 Auth (Firebase Auth)

* Providers: Email link (passwordless) + Google.
* Flow: anonymous quick submit → optional link to email to claim later.
* Security: verify ID tokens server‑side on protected routes.

### 3.3 Database (Firestore in Datastore mode)

* **Kinds**: `User`, `Character`, `Spot`, `Hunt`, `HuntParticipant`, `HuntMetrics`, `AnalyzerUpload`, `SpotAggregate`.
* **Indexes**: keep minimal; composite indexes only for the main list filters.
* **Access**: App Engine default service account (least privilege). Use IAM to restrict.

### 3.4 Storage (GCS)

* Bucket: default App Engine bucket.
* Store original Analyzer text as small `.txt` objects; keep parsed fields in DB.
* Public images (future) behind cached URLs; private uploads via signed URLs.

### 3.5 Jobs & Aggregations

* App Engine Cron (daily): recompute `SpotAggregate` (avg XP/hr, Profit/hr, sample size, last seen, by party comp & vocation).
* Optional Cloud Tasks queue if aggregation per‑spot might exceed request time.
