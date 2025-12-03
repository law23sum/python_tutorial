
from tutorial.apps.topics.views import TopicDetailView


class WebHomeView(TopicDetailView):
    topic_slug = "web"
