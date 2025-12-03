
from django.urls import path

from .views import AlgorithmsHomeView

app_name = "tutorial_algorithms"

urlpatterns = [
    path("", AlgorithmsHomeView.as_view(), name="home"),
]
