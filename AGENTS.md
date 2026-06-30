# National Drug Observatory (Liberia)

Django 6.0 project — multi-agency drug data system for Liberia. Built by Charles E S Boimah.

## Quick start

```powershell
python manage.py runserver        # dev server (DEBUG=True, SQLite)
python manage.py makemigrations   # after model changes
python manage.py migrate          # apply migrations
python manage.py createsuperuser  # admin access
```

No `requirements.txt` exists. Dependencies (inferred from imports): Django 6.0+, `django-user-agents`, `Pillow`, `whitenoise`.

## Apps & ownership

| App | Agency | Purpose |
|-----|--------|---------|
| `accounts` | Central | CustomUser (email auth via `EmailBackend`), per-agency profile models, role-based redirect |
| `ldea` | Liberia Drug Enforcement Agency | Raids, drug types, seizures, arrests, persons, cases, evidence, victim histories |
| `moj` | Ministry of Justice | Court case updates, victim referral to MoH, IT admin (creates users for all agencies) |
| `moh` | Ministry of Health | Treatment facilities, demand reduction, prevention activities |
| `mog` | Ministry of Gender | Child assessments, family tracing, follow-up visits, case closures |
| `moys` | Ministry of Youth & Sports | **Placeholder** — empty models.py |

## Auth & routes

- Login uses **email** (not username), driven by `accounts.backend.EmailBackend`
- 12 roles total (`moj_head`, `moj_officers`, `moj_it_head`, `ldea_head`, `officers`, `ldea_head_of_it`, `moh_head`, `moh_officers`, `mog_head`, `mog_officers`, `moys_head`, `moys_officers`)
- Role-based redirect after login via `ROLE_REDIRECTS` dict in `accounts/views.py`
- All app URLs mounted at root (`''`) in `national_drug_obs/urls.py`
- URL convention: `national/drug/observatory/{agency}/{role}/...`

## Key config in `settings.py`

| Setting | Value |
|---------|-------|
| `AUTH_USER_MODEL` | `accounts.CustomUser` |
| `AUTHENTICATION_BACKENDS` | `accounts.backend.EmailBackend` first, then `ModelBackend` |
| `STATICFILES_DIRS` | `static/` |
| `STATIC_ROOT` | `staticfiles/` |
| `STATICFILES_STORAGE` | whitenoise (wired as string literal — not imported properly) |
| Database | SQLite (`db.sqlite3`) |
| Templates | `templates/` (Phoenix bootstrap theme) |

## MoYS app

The `moys` app has an empty `models.py` and no `urls.py`. It's registered in `INSTALLED_APPS` but unused.

## Tests

All apps ship stock Django `tests.py`. No actual tests written. No test runner config.

## No CI / lint / formatter / typechecker

None configured. No `requirements.txt`, `pyproject.toml`, or `Pipfile`.

## Migrations

Migrations exist for all apps with data. Use `python manage.py makemigrations` before `migrate` after model edits.
