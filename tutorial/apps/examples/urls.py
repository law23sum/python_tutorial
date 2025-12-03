from django.urls import path

from .views import ExamplesHomeView

app_name = "tutorial_examples"

urlpatterns = [
    path("", ExamplesHomeView.as_view(), name="home"),
]
