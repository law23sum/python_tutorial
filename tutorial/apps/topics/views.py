
from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from tutorial.apps.topics.registry import TOPICS, get_topic


def _build_topic(slug: str):
    topic = get_topic(slug)
    topic.setdefault("tagline", topic["slug"].replace("_", " ").replace("-", " ").title())
    return topic


class TopicDetailView(TemplateView):
    template_name = "tutorial/topics/topic_detail.html"
    topic_slug: str = ""

    def get_topic(self):
        if not self.topic_slug:
            raise ValueError("topic_slug must be set on TopicDetailView")
        return _build_topic(self.topic_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_topic()
        context.setdefault("topic", topic)
        context.setdefault("topics", [_build_topic(entry["slug"]) for entry in TOPICS])
        context.setdefault("active_tab", "tutorial")
        return context


class TutorialHomeView(TemplateView):
    template_name = "tutorial/topics/tutorial_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("topics", [_build_topic(entry["slug"]) for entry in TOPICS])
        context.setdefault("active_tab", "tutorial")
        context.setdefault("page_title", _("Python Tutorial"))
        return context
