
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevopsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.devops"
    label = "tutorial_devops"
    verbose_name = _("DevOps")
