from django.conf import settings

NAV = [
    ("Services", "/services/"),
    ("Work", "/work/"),
    ("Products", "/products/"),
    ("Insights", "/insights/"),
    ("About", "/about/"),
]


def site(request):
    path = request.path
    return {
        "company": settings.COMPANY,
        "site_url": settings.SITE_URL,
        "nav": [{"label": l, "url": u, "active": path.startswith(u)} for l, u in NAV],
    }
