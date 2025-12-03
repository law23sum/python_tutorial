
from django.urls import path

from .views import FoundationsHomeView

app_name = "tutorial_foundations"

urlpatterns = [
    path("", FoundationsHomeView.as_view(), name="home"),
]
