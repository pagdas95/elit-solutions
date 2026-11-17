import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from . import content
from .forms import ContactForm

log = logging.getLogger(__name__)

PROCESS = [
    ("Discover", "We map the problem, the people involved and what success looks like, before any code."),
    ("Design", "Flows, interfaces and architecture you can see and react to early."),
    ("Build", "Short iterations, working software every week or two, tested as we go."),
    ("Run", "Launch, monitoring and support, so it keeps working after go-live."),
]


def home(request):
    return render(request, "web/home.html", {
        "services": content.collection("services"),
        "work": content.collection("work")[:3],
        "posts": content.collection("blog")[:3],
        "process": PROCESS,
    })


def services(request):
    return render(request, "web/services.html", {"services": content.collection("services"), "process": PROCESS})


def service_detail(request, slug):
    entry = content.get("services", slug)
    others = [s for s in content.collection("services") if s.slug != slug]
    related = [w for w in content.collection("work") if slug in (w.meta.get("services") or [])]
    return render(request, "web/service_detail.html", {"entry": entry, "others": others, "related": related})


def work(request):
    return render(request, "web/work.html", {"work": content.collection("work")})


def work_detail(request, slug):
    entry = content.get("work", slug)
    services = {s.slug: s for s in content.collection("services")}
    return render(request, "web/work_detail.html", {
        "entry": entry, "services": [services[s] for s in entry.meta.get("services", []) if s in services]})


def insights(request):
    return render(request, "web/insights.html", {"posts": content.collection("blog")})


def insight_detail(request, slug):
    entry = content.get("blog", slug)
    more = [p for p in content.collection("blog") if p.slug != slug][:2]
    return render(request, "web/insight_detail.html", {"entry": entry, "more": more})


def products(request):
    return render(request, "web/page.html", {"entry": content.page("products"), "variant": "products"})


def about(request):
    return render(request, "web/page.html", {"entry": content.page("about"), "variant": "about",
                                             "process": PROCESS})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                log.info("contact form: honeypot filled, discarded")
            else:
                d = form.cleaned_data
                body = "\n".join(f"{form.fields[k].label or k.title()}: {d.get(k) or '-'}"
                                 for k in ("name", "email", "company", "service", "budget"))
                send_mail(subject=f"[Website] New enquiry from {d['name']}",
                          message=f"{body}\n\n{d['message']}",
                          from_email=settings.DEFAULT_FROM_EMAIL,
                          recipient_list=settings.CONTACT_RECIPIENTS, fail_silently=False)
            messages.success(request, "Thanks, your message is on its way. We reply within one working day.")
            return redirect("contact")
    else:
        initial = {"service": request.GET.get("service", "")}
        form = ContactForm(initial=initial)
    return render(request, "web/contact.html", {"form": form})


@require_GET
def robots_txt(request):
    lines = ["User-agent: *", "Allow: /", f"Sitemap: {settings.SITE_URL}/sitemap.xml"]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def not_found(request, exception=None):
    return render(request, "404.html", status=404)
