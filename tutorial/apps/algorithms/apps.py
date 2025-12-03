
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AlgorithmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.algorithms"
    label = "tutorial_algorithms"
    verbose_name = _("Algorithms")
