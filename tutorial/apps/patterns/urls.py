
from django.urls import path

from .views import PatternsHomeView

app_name = "tutorial_patterns"

urlpatterns = [
    path("", PatternsHomeView.as_view(), name="home"),
]
