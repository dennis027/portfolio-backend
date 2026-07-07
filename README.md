# Portfolio Backend

Production-ready Django + DRF backend for Dennis Kimani's portfolio (Angular frontend).

## Stack
Django 5, DRF, PostgreSQL, SimpleJWT, drf-spectacular (Swagger/Redoc), django-filter,
CORS headers, WhiteNoise, Gunicorn, Docker.

## Project layout
```
config/            settings, root urls, wsgi/asgi
apps/
  accounts/         JWT login (wraps SimpleJWT)
  contact/          public contact form + admin inbox
  analytics/        visitor tracking + dashboard aggregation
  portfolio/        projects, skills, experience, education, certifications,
                     testimonials, newsletter, blog, resume tracking, GitHub activity,
                     combined admin dashboard
middleware/         VisitorTrackingMiddleware (auto-records every request)
utils/              shared response envelope, exception handler, client-info parsing
tests/              APITestCase suites
nginx/              reverse-proxy config for prod
```

## Quick start (local, no Docker)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then edit DB + email + recaptcha values
createdb portfolio_db       # or let Docker's postgres container do it
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Quick start (Docker)
```bash
cp .env.example .env
docker compose up --build
```
Services: `web` (Django/Gunicorn), `db` (Postgres 16), `nginx` (reverse proxy on :80),
`pgadmin` (:5050, optional).

## Key endpoints
- `POST /api/auth/login/`, `POST /api/auth/refresh/` — JWT
- `POST /api/contact/` (public) · `GET/PATCH/DELETE /api/contact/{id}/` (admin)
- `GET /api/analytics/dashboard/`, `GET /api/analytics/recent/` (admin)
- `GET /api/dashboard/` — combined admin dashboard summary
- `GET/POST /api/projects/`, `/api/skills/`, `/api/experience/`, `/api/education/`,
  `/api/certifications/` (public read, admin write)
- `GET/POST /api/testimonials/` (public submit + admin-approved public list)
- `POST /api/newsletter/` (public subscribe)
- `GET/POST /api/blog/` (public published posts, admin full CRUD)
- `POST /api/resume/track/` — increment CV download counter
- `GET /api/github/activity/` — recent public repos
- `GET /health/` — `{"status": "healthy"}`
- `GET /api/docs/` (Swagger), `/api/redoc/` (Redoc), `/api/schema/` (raw OpenAPI)

## Response envelope
Every endpoint returns `{ "success": bool, "message": str, "data": any }`,
including error responses (see `utils/exceptions.py`).

## Visitor tracking
`middleware/visitor_tracking.py` records IP, browser, OS, device type,
referrer, landing page, and page visits for every non-admin/static request —
no frontend instrumentation required. Session-based, so returning visitors
(`visit_count > 1`) are tracked automatically.

## Security
JWT auth, CORS allow-list, CSRF trusted origins, DRF throttling (global +
a stricter `contact_form` scope), honeypot field + optional reCAPTCHA v3 on
the contact form, HSTS/SSL redirect/secure cookies auto-enabled when `DEBUG=False`.

## Tests
```bash
python manage.py test tests
```

## Suggested next steps
- Add a `country`/`city` GeoIP lookup (e.g. MaxMind GeoLite2) to populate
  `Visitor.country`/`city` and `Contact.country` automatically from IP.
- Wire the Angular app's CV download button to call `POST /api/resume/track/`
  right before triggering the file download.
- Point `GITHUB_USERNAME`/`GITHUB_TOKEN` in `.env` to raise GitHub's rate limit.
# portfolio-backend
