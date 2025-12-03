
from django.urls import path

from .views import SystemDesignHomeView

app_name = "tutorial_system_design"

urlpatterns = [
    path("", SystemDesignHomeView.as_view(), name="home"),
]
