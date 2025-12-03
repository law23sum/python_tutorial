
from tutorial.apps.topics.views import TopicDetailView


class AsyncHomeView(TopicDetailView):
    topic_slug = "async"
