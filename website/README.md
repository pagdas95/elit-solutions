# ElIT Solutions website

Django 5.2 site for ElIT Solutions, built on the final brand (`brand/final/`). Dark-first, English, no database yet:
content lives in Markdown files.

## Run it locally

```bash
uv venv .venv && uv pip install --python .venv/bin/python -r website/requirements.txt
cd website
../.venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000. Contact-form e-mails print to the terminal in development.

Tests: `../.venv/bin/python manage.py test`

## Pages

Home · Services (+ one page per service) · Work (+ case studies) · Products · Insights (+ articles) · About · Contact
(enquiry form with validation and a spam honeypot) · sitemap.xml · robots.txt · 404.

## Editing content

All text is in `content/` as Markdown with a small header (front matter):

| Folder | One file per | Header fields |
|---|---|---|
| `content/services/` | service | `title`, `summary`, `order`, `icon` (web · software · automation · integration), `includes`, `stack` |
| `content/work/` | case study | `title`, `client`, `sector`, `summary`, `services`, `year`, `order`, `placeholder`, `outcomes` |
| `content/blog/` | article | `title`, `summary`, `date` (YYYY-MM-DD), `author`, `tags`, `draft` |
| `content/pages/` | page | `title`, `summary` (`about.md`, `products.md`) |

The file name is the URL: `content/blog/my-post.md` → `/insights/my-post/`. Set `draft: true` to hide an article.
Quote list items that contain a colon (`- "Step one: plan"`); a test checks this.

**Before launch:** the three case studies in `content/work/` are clearly labelled examples (`placeholder: true`).
Replace them with real projects, with each client's permission, or remove them.

## Configuration (environment variables)

| Variable | Purpose |
|---|---|
| `DJANGO_DEBUG` | `false` in production |
| `DJANGO_SECRET_KEY` | required in production |
| `DJANGO_ALLOWED_HOSTS` | e.g. `elitsolutions.com,www.elitsolutions.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | e.g. `https://elitsolutions.com` |
| `ELIT_SITE_URL` | public URL, used in canonical links, Open Graph and the sitemap |
| `ELIT_PUBLIC_EMAIL`, `ELIT_PUBLIC_PHONE`, `ELIT_LINKEDIN_URL`, `ELIT_LOCATION` | contact details shown on the site (hidden while empty) |
| `ELIT_CONTACT_RECIPIENTS` | who receives contact-form messages (comma list) |
| `DJANGO_EMAIL_BACKEND`, `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_HOST_USER`, `DJANGO_EMAIL_HOST_PASSWORD` | SMTP for sending the contact form |

For production: run `manage.py collectstatic`, serve with a WSGI server (e.g. gunicorn), and serve `staticfiles/`
from the web server or add WhiteNoise.

## Later: Django admin

The front-matter fields map one-to-one onto models (Service, CaseStudy, Article, Page). To add the admin: configure a
database, create those models, import the Markdown files once with a management command, and switch
`web/content.py` to read from the models.

## Design notes

- Fonts are self-hosted (`static/fonts/`, OFL), so visitors' IP addresses are not sent to Google.
- Colour, type and graphics follow `brand/final/`; the background pattern and service icons are drawn from the
  logo's isometric slabs.
- Accessibility: skip link, visible focus styles, AA text contrast on Midnight, reduced-motion support, and a
  navigation that works without JavaScript.
