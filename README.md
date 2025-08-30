# TibiaHunts

[![Code Quality Check](https://github.com/Vichoko/tibia-hunts/actions/workflows/code-quality.yml/badge.svg)](https://github.com/Vichoko/tibia-hunts/actions/workflows/code-quality.yml)
[![Django Tests](https://github.com/Vichoko/tibia-hunts/actions/workflows/django-tests.yml/badge.svg)](https://github.com/Vichoko/tibia-hunts/actions/workflows/django-tests.yml)
[![PR Title Check](https://github.com/Vichoko/tibia-hunts/actions/workflows/pr-title-check.yml/badge.svg)](https://github.com/Vichoko/tibia-hunts/actions/workflows/pr-title-check.yml)
[![Release](https://github.com/Vichoko/tibia-hunts/actions/workflows/release.yml/badge.svg)](https://github.com/Vichoko/tibia-hunts/actions/workflows/release.yml)

A community platform for Tibia players to register and share hunting sessions, building a collaborative dataset of hunting spots.

## 🎯 Project Goals

- **Register hunts**: Log hunting sessions with metrics (XP/hr, profit/hr, etc.)
- **Community spots database**: Crowdsourced hunting locations with aggregated data
- **Hunt Analyzer integration**: Parse and import Hunt Analyzer output
- **Smart recommendations**: Find the best spots for your level/vocation/setup

## 🚀 Features (MVP)

- ✅ Submit hunting sessions with participants and metrics
- ✅ Browse and search hunting spots
- ✅ Character pages with hunting history
- ✅ Hunt Analyzer output parsing
- ✅ Community-driven spot data
- ✅ **Google OAuth Authentication** - Sign in with your Google account

## 🛠️ Tech Stack

- **Backend**: Django 5.2 (Python 3.11+)
- **Authentication**: django-allauth with Google OAuth
- **Code Quality**: Ruff (linting & formatting)
- **CI/CD**: GitHub Actions with semantic-release
- **Database**: SQLite (development), PostgreSQL (production)

## 📋 Development

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development workflow and pull request guidelines.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Vichoko/tibia-hunts.git
cd tibia-hunts

# Install dependencies
poetry install

# Run development server
poetry run python src/manage.py runserver
```

### Quick Start: Google Login (Local)

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Create Google OAuth credentials**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google+ API
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google OAuth credentials:
   # GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   # GOOGLE_CLIENT_SECRET=your-client-secret
   ```

4. **Run migrations and start server**:
   ```bash
   cd src
   python manage.py migrate
   python manage.py runserver
   ```

5. **Test the authentication**:
   - Browse to http://localhost:8000/
   - Click "Sign in with Google"
   - Complete OAuth flow
   - Visit http://localhost:8000/api/me to confirm authentication

### Code Quality

```bash
# Check linting and formatting
poetry run ruff check .
poetry run ruff format --check .

# Run tests
poetry run python src/manage.py test

# Django system checks
poetry run python src/manage.py check
```

## 📖 Documentation

- [RFC v0.1](rfc/v0.1.md) - Complete project specification and architecture
- [Contributing Guide](docs/CONTRIBUTING.md) - Development workflow and guidelines

## 📄 License

This project is open source. See the project details for more information.

---

Built with ❤️ for the Tibia community
