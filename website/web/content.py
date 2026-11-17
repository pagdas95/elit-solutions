"""Markdown content: content/<collection>/<slug>.md with YAML front matter.

Front-matter fields map 1:1 onto future Django models, so moving to the Django admin later means creating models with
these fields and importing the files once. Collections:

  services  title, summary, order, icon, includes[], stack[]
  work      title, client, sector, summary, services[], year, order, placeholder (bool), outcomes[]
  blog      title, summary, date (YYYY-MM-DD), author, tags[], draft (bool)
  pages     title, summary (about, products, ...)
"""
import datetime
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import frontmatter
import markdown
from django.conf import settings
from django.http import Http404

MD_EXTENSIONS = ["extra", "sane_lists", "smarty", "toc"]


@dataclass
class Entry:
    collection: str
    slug: str
    meta: dict
    body_html: str
    words: int = 0
    extra: dict = field(default_factory=dict)

    def __getattr__(self, name):  # template access: entry.title, entry.summary ...
        try:
            return self.meta[name]
        except KeyError:
            raise AttributeError(name) from None

    @property
    def reading_minutes(self):
        return max(1, round(self.words / 220))

    def get_absolute_url(self):
        return {"services": f"/services/{self.slug}/", "work": f"/work/{self.slug}/",
                "blog": f"/insights/{self.slug}/"}.get(self.collection, f"/{self.slug}/")


def _load(path: Path, collection: str) -> Entry:
    post = frontmatter.load(path)
    meta = dict(post.metadata)
    if isinstance(meta.get("date"), str):
        meta["date"] = datetime.date.fromisoformat(meta["date"])
    html = markdown.markdown(post.content, extensions=MD_EXTENSIONS, output_format="html")
    return Entry(collection, path.stem, meta, html, words=len(post.content.split()))


def _collection(name: str) -> tuple:
    folder = Path(settings.CONTENT_DIR) / name
    entries = [_load(p, name) for p in sorted(folder.glob("*.md"))]
    if name == "blog":
        entries = [e for e in entries if not e.meta.get("draft")]
        entries.sort(key=lambda e: e.meta.get("date") or datetime.date.min, reverse=True)
    else:
        entries.sort(key=lambda e: (e.meta.get("order", 999), e.slug))
    return tuple(entries)


_cached = lru_cache(maxsize=None)(_collection)


def collection(name: str) -> tuple:
    """All entries of a collection. Re-read on every request in DEBUG, so edits show up immediately."""
    return _collection(name) if settings.DEBUG else _cached(name)


def get(name: str, slug: str) -> Entry:
    for e in collection(name):
        if e.slug == slug:
            return e
    raise Http404(f"No {name} entry '{slug}'")


def page(slug: str) -> Entry:
    return get("pages", slug)
