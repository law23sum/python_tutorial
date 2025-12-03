
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.oop"
    label = "tutorial_oop"
    verbose_name = _("Object-Oriented Programming")
