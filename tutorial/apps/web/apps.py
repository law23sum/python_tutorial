
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WebConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.web"
    label = "tutorial_web"
    verbose_name = _("Web")
