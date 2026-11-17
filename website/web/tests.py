from django.core import mail
from django.test import SimpleTestCase, override_settings

from . import content

PAGES = ["/", "/services/", "/work/", "/products/", "/insights/", "/about/", "/contact/"]

VALID = {"name": "Maria", "email": "maria@example.com", "company": "Example Ltd", "service": "software",
         "budget": "5-15", "message": "We need a portal for our customers to track orders."}


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                   CONTACT_RECIPIENTS=["team@example.com"])
class SiteTests(SimpleTestCase):
    def test_static_pages_render(self):
        for url in PAGES:
            with self.subTest(url=url):
                r = self.client.get(url)
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, "ElIT Solutions")

    def test_every_content_entry_renders(self):
        for name, prefix in (("services", "/services/"), ("work", "/work/"), ("blog", "/insights/")):
            entries = content.collection(name)
            self.assertTrue(entries, name)
            for e in entries:
                with self.subTest(url=e.get_absolute_url()):
                    r = self.client.get(e.get_absolute_url())
                    self.assertEqual(r.status_code, 200)
                    self.assertContains(r, e.title)

    def test_placeholder_case_studies_are_labelled(self):
        for e in content.collection("work"):
            if e.meta.get("placeholder"):
                self.assertContains(self.client.get(e.get_absolute_url()), "Example case study")

    def test_unknown_pages_404(self):
        self.assertEqual(self.client.get("/services/nope/").status_code, 404)
        self.assertEqual(self.client.get("/does-not-exist/").status_code, 404)

    def test_contact_form_sends_email(self):
        r = self.client.post("/contact/", VALID, follow=True)
        self.assertContains(r, "on its way")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Maria", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ["team@example.com"])
        self.assertIn("portal", mail.outbox[0].body)

    def test_contact_form_validates(self):
        r = self.client.post("/contact/", {**VALID, "email": "not-an-email", "message": "short"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "field-error")
        self.assertEqual(len(mail.outbox), 0)

    def test_honeypot_discards_spam_silently(self):
        r = self.client.post("/contact/", {**VALID, "website": "http://spam.example"}, follow=True)
        self.assertContains(r, "on its way")
        self.assertEqual(len(mail.outbox), 0)

    def test_service_preselected_from_query(self):
        r = self.client.get("/contact/?service=automation")
        self.assertContains(r, '<option value="automation" selected>')

    def test_sitemap_and_robots(self):
        s = self.client.get("/sitemap.xml")
        self.assertEqual(s.status_code, 200)
        self.assertContains(s, "/insights/automate-first/")
        self.assertContains(self.client.get("/robots.txt"), "Sitemap:")

    def test_list_fields_are_plain_strings(self):
        # A colon inside an unquoted YAML list item turns it into a dict ("- Key: value"); quote such items.
        for name in ("services", "work", "blog"):
            for e in content.collection(name):
                for key, value in e.meta.items():
                    if isinstance(value, list):
                        for item in value:
                            with self.subTest(entry=f"{name}/{e.slug}", field=key):
                                self.assertIsInstance(item, (str, int), item)

    def test_blog_sorted_newest_first(self):
        dates = [p.date for p in content.collection("blog")]
        self.assertEqual(dates, sorted(dates, reverse=True))
