from django.urls import path

from .views import TutorialHomeView

app_name = "tutorial_topics"

urlpatterns = [
    path("", TutorialHomeView.as_view(), name="home"),
]
