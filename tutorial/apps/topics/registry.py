from __future__ import annotations

from typing import Dict, List

from django.utils.translation import gettext_lazy as _

Topic = Dict[str, str]

TOPICS: List[Topic] = [
    {"slug": "foundations", "title": _("Foundations"), "summary": _("Master Python syntax, packaging, and essential tooling.")},
    {"slug": "data_structures", "title": _("Data Structures"), "summary": _("Practice working with built-in collections and custom containers.")},
    {"slug": "algorithms", "title": _("Algorithms"), "summary": _("Implement search, sorting, and optimization routines in Python.")},
    {"slug": "oop", "title": _("Object-Oriented Programming"), "summary": _("Design classes, protocols, and inheritance hierarchies with clarity.")},
    {"slug": "patterns", "title": _("Patterns"), "summary": _("Apply proven software design patterns using idiomatic Python.")},
    {"slug": "web", "title": _("Web"), "summary": _("Build user-facing experiences with Django views, templates, and reactive interfaces.")},
    {"slug": "db", "title": _("Databases"), "summary": _("Model relational data with the ORM and reason about migrations and queries.")},
    {"slug": "api", "title": _("APIs"), "summary": _("Expose and consume HTTP services with Django REST Framework and typed clients.")},
    {"slug": "async", "title": _("Async"), "summary": _("Write reliable asynchronous workers, message consumers, and network clients.")},
    {"slug": "devops", "title": _("DevOps"), "summary": _("Automate deployments, infrastructure configuration, and observability.")},
    {"slug": "system_design", "title": _("System Design"), "summary": _("Plan resilient architectures and scalability strategies before coding.")},
    {"slug": "tests", "title": _("Tests"), "summary": _("Develop rigorous automated tests with pytest, Django, and contract checks.")},
    {"slug": "leadership", "title": _("Leadership"), "summary": _("Guide teams with process, mentorship, and clear communication.")},
]

def get_topic(slug: str) -> Topic:
    for topic in TOPICS:
        if topic["slug"] == slug:
            topic = topic.copy()
            topic.setdefault("url_name", f"tutorial_{slug}:home")
            return topic
    raise KeyError(slug)
