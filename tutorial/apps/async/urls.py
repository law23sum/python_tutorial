
from django.urls import path

from .views import AsyncHomeView

app_name = "tutorial_async"

urlpatterns = [
    path("", AsyncHomeView.as_view(), name="home"),
]
