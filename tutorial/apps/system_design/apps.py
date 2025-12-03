
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SystemDesignConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.system_design"
    label = "tutorial_system_design"
    verbose_name = _("System Design")
