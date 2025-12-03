
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AsyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutorial.apps.async"
    label = "tutorial_async"
    verbose_name = _("Async")
