
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DataStructuresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.data_structures"
    label = "tutorial_data_structures"
    verbose_name = _("Data Structures")
