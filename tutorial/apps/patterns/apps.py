
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatternsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.patterns"
    label = "tutorial_patterns"
    verbose_name = _("Patterns")
