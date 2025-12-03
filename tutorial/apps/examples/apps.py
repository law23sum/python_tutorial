from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExamplesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.examples"
    verbose_name = _("Tutorial Examples")
