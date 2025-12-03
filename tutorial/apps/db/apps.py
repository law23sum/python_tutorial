
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.db"
    label = "tutorial_db"
    verbose_name = _("Databases")
