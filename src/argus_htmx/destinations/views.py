from typing import Optional
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from rest_framework.exceptions import ValidationError

from argus.notificationprofile.models import DestinationConfig
from argus.notificationprofile.media import api_safely_get_medium_object
from argus.notificationprofile.media.base import NotificationMedium

from .forms import DestinationFormCreate, DestinationFormUpdate


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
    return _render_destinations(request, create_form=form)


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


@require_http_methods(["POST"])
def destinations_update(request, pk: int) -> HttpResponse:
    destination = DestinationConfig.objects.get(pk=pk)
    form = DestinationFormUpdate(request.POST or None, instance=destination, request=request)
    if form.is_valid():
        form.save()
    return _render_destinations(request)


def _render_destinations(request, create_form: Optional[DestinationFormCreate] = None) -> HttpResponse:
    """Function to render the destinations page.

    :param create_form: this is used to display the form for creating a new destination
    with errors while retaining the user input. If you want a blank form, pass None."""
    if create_form is None:
        create_form = DestinationFormCreate()
    context = {
        "create_form": create_form,
    }
    return render(request, "htmx/destinations/destinations.html", context=context)
