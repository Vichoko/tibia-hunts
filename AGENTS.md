# TibiaHunts

A community platform for Tibia players to register and share hunting sessions, building a collaborative dataset of hunting spots.

## Architecture

- **Frontend + Backend**: Google App Engine Standard (Python 3.11) with Django 5.2
- **Database**: SQLite (local file) for MVP — zero external DB costs
- **Auth**: Google OAuth via django-allauth
- **Static Files**: Served through App Engine with 1-hour caching
- **Deployment**: Single `app.yaml` with scale-to-zero settings

```
[ Browser ] → [ App Engine (Python 3.11) ] → [ Django App ] → [ SQLite ]
                                          → [ Static Files → 1h Cache ]
```

## Core Principles

- **MVP first**: Create, view, and search hunts. Frictionless submission (anonymous + later claim).
- **Open data**: Spots (locations/spawns) are community-editable.
- **Analyzer-friendly**: Support pasting Hunt Analyzer output and parse key stats.
- **Extensible**: Schemas & APIs designed for future ranking/recommendations.
- **Cost-efficient**: Scale-to-zero, single instance, SQLite ($0/month).

## Tech Stack

| Layer         | Technology                  |
|---------------|-----------------------------|
| Language      | Python 3.11                 |
| Web Framework | Django 5.2                  |
| Auth          | django-allauth (Google OAuth) |
| Database      | SQLite (MVP, zero-cost) |
| Linting       | Ruff (strict ruleset)       |
| Packaging     | Poetry                      |
| CI/CD         | GitHub Actions + semantic-release |
| Deployment    | Google App Engine Standard  |

## Development Conventions

### Branch Strategy
- Feature branches: `feat/<description>`, `fix/<description>`
- All changes land via PR to `main`
- Never push directly to `main`

### Commit Style
Conventional Commits (Angular preset):

```
feat: add hunt submission form
fix(auth): resolve Google OAuth redirect
docs: update API docs
chore(deps): update django to 5.2
```

### Commit Types
`feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

## CI/CD Pipeline

| Workflow | Triggers |
|----------|----------|
| Code Quality | PRs — Ruff lint + format check + Django system check |
| Django Tests | PRs — migration checks + unit tests |
| PR Title Check | PRs — validates conventional commit format |
| PR Title Validation | PRs — additional title format validation |
| Release | Push to main — semantic-release, changelog, version bump |
| Deploy | Release complete — deploy to GAE |

## Code Quality Expectations

```bash
# Linting & formatting
poetry run ruff check .
poetry run ruff format --check .

# Django checks
poetry run python src/manage.py check

# Tests
poetry run python src/manage.py test

# Apply auto-fixes
poetry run ruff check . --fix
poetry run ruff format .
```

## Agent Environment

- **OS**: Linux
- **Shell**: bash
- **Agent**: Hermes Agent (Nous Research)
- **GitHub bot**: Vichokobot
- **Default branch**: `main`
- **Repo**: https://github.com/Vichoko/tibia-hunts
