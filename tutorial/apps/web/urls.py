
from django.urls import path

from .views import WebHomeView

app_name = "tutorial_web"

urlpatterns = [
    path("", WebHomeView.as_view(), name="home"),
]
