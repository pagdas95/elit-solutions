from django.contrib.sitemaps import Sitemap

from . import content

STATIC_PATHS = ["/", "/services/", "/work/", "/products/", "/insights/", "/about/", "/contact/"]


class StaticSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return STATIC_PATHS

    def location(self, item):
        return item


class ContentSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return [*content.collection("services"), *content.collection("work"), *content.collection("blog")]

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.meta.get("date")
