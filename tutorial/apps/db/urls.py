
from django.urls import path

from .views import DbHomeView

app_name = "tutorial_db"

urlpatterns = [
    path("", DbHomeView.as_view(), name="home"),
]
