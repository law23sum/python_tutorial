
from tutorial.apps.topics.views import TopicDetailView


class ApiHomeView(TopicDetailView):
    topic_slug = "api"
