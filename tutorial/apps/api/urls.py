
from django.urls import path

from .views import ApiHomeView

app_name = "tutorial_api"

urlpatterns = [
    path("", ApiHomeView.as_view(), name="home"),
]
