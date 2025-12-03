
from django.urls import path

from .views import LeadershipHomeView

app_name = "tutorial_leadership"

urlpatterns = [
    path("", LeadershipHomeView.as_view(), name="home"),
]
