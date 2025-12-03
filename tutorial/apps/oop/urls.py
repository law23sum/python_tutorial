
from django.urls import path

from .views import OopHomeView

app_name = "tutorial_oop"

urlpatterns = [
    path("", OopHomeView.as_view(), name="home"),
]
