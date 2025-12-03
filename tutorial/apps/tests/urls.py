
from django.urls import path

from .views import TestsHomeView

app_name = "tutorial_tests"

urlpatterns = [
    path("", TestsHomeView.as_view(), name="home"),
]
