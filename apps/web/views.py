from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def home(request):
    if request.user.is_authenticated:
        return render(
            request,
            "web/app_home.html",
            context={
                "active_tab": "python_tutorial",
                "page_title": _("python_tutorial"),
            },
        )
    else:
        return render(request, "web/landing_page.html")


def simulate_error(request):
    raise Exception("This is a simulated error.")