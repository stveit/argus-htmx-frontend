from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .forms import DestinationFormCreate


@require_http_methods(["GET", "POST"])
def destinations(request):
    if request.method == "GET":
        return _render_destinations(request)
    elif request.method == "POST":
        return destinations_create(request)


def destinations_create(request) -> HttpResponse:
    form = DestinationFormCreate(request.POST or None, request=request)
    if form.is_valid():
        form.save()
    return _render_destinations(request)

def _render_destinations(request) -> HttpResponse:
    return render(request, "htmx/destinations/destinations.html")
