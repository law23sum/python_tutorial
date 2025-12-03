from __future__ import annotations

from dataclasses import dataclass
from typing import List

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from tutorial.apps.topics.registry import get_topic


@dataclass(frozen=True)
class ExampleCard:
    slug: str
    title: str
    summary: str
    url_name: str
    icon: str
    focus: str
    level: str


EXAMPLE_DETAILS = {
    "db": {
        "icon": "fa-solid fa-database",
        "focus": _("Schema design, migrations, and query analysis."),
        "level": _("Intermediate"),
    },
    "oop": {
        "icon": "fa-solid fa-diagram-project",
        "focus": _("Model business domains with clear class hierarchies."),
        "level": _("Core"),
    },
    "system_design": {
        "icon": "fa-solid fa-sitemap",
        "focus": _("Plan architecture trade-offs before writing code."),
        "level": _("Advanced"),
    },
}


class ExamplesHomeView(TemplateView):
    template_name = "tutorial/examples/examples_home.html"
    example_slugs: List[str] = ["db", "oop", "system_design"]

    def get_examples(self) -> list[ExampleCard]:
        examples: list[ExampleCard] = []
        for slug in self.example_slugs:
            topic = get_topic(slug)
            extra = EXAMPLE_DETAILS.get(slug, {})
            examples.append(
                ExampleCard(
                    slug=slug,
                    title=str(topic["title"]),
                    summary=str(topic["summary"]),
                    url_name=topic["url_name"],
                    icon=str(extra.get("icon", "fa-solid fa-lightbulb")),
                    focus=str(extra.get("focus", "")),
                    level=str(extra.get("level", "")),
                )
            )
        return examples

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("examples", self.get_examples())
        context.setdefault("page_title", _("Tutorial Examples"))
        context.setdefault("active_tab", "tutorial")
        return context
