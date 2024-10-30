from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from rest_framework.exceptions import ValidationError

from argus.notificationprofile.media import api_safely_get_medium_object
from argus.notificationprofile.media.base import NotificationMedium

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


@require_http_methods(["POST"])
def destinations_delete(request, pk: int) -> HttpResponse:
    destination = get_object_or_404(request.user.destinations.all(), pk=pk)

    try:
        medium = api_safely_get_medium_object(destination.media.slug)
        medium.raise_if_not_deletable(destination)
    except NotificationMedium.NotDeletableError as e:
        raise ValidationError(str(e))
    else:
        destination.delete()
        return _render_destinations(request)


def _render_destinations(request) -> HttpResponse:
    return render(request, "htmx/destinations/destinations.html")
