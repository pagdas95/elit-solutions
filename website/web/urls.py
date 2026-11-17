from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import ContentSitemap, StaticSitemap

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service"),
    path("work/", views.work, name="work"),
    path("work/<slug:slug>/", views.work_detail, name="work_detail"),
    path("insights/", views.insights, name="insights"),
    path("insights/<slug:slug>/", views.insight_detail, name="insight"),
    path("products/", views.products, name="products"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("robots.txt", views.robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": StaticSitemap, "content": ContentSitemap}},
         name="django.contrib.sitemaps.views.sitemap"),
]
