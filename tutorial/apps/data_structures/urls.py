
from django.urls import path

from .views import DataStructuresHomeView

app_name = "tutorial_data_structures"

urlpatterns = [
    path("", DataStructuresHomeView.as_view(), name="home"),
]
