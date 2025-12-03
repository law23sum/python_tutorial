
from django.urls import path

from .views import DevopsHomeView

app_name = "tutorial_devops"

urlpatterns = [
    path("", DevopsHomeView.as_view(), name="home"),
]
