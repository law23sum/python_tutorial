
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FoundationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.foundations"
    label = "tutorial_foundations"
    verbose_name = _("Foundations")
