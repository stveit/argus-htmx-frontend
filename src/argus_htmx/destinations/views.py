from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


@require_http_methods(["GET"])
def destinations(request) -> HttpResponse:
    return _render_destinations


def _render_destinations(request) -> HttpResponse:
    return render(request, "htmx/destinations/destinations.html")
