
from tutorial.apps.topics.views import TopicDetailView


class DbHomeView(TopicDetailView):
    topic_slug = "db"
