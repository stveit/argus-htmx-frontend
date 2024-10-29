from __future__ import annotations
from typing import Optional

from django.shortcuts import redirect, render, get_object_or_404

from django.http import HttpResponse

from django.views.decorators.http import require_POST, require_http_methods

from rest_framework.exceptions import ValidationError

from argus.notificationprofile.models import DestinationConfig, Media
from argus.notificationprofile.media import api_safely_get_medium_object
from argus.notificationprofile.serializers import RequestDestinationConfigSerializer
from argus.notificationprofile.media.base import NotificationMedium

from .forms import DestinationFormCreate, DestinationFormUpdate


@require_http_methods(["GET", "POST"])
def destinations(request) -> HttpResponse:
    if request.method == "GET":
        return destinations_list(request, DestinationFormCreate())
    elif request.method == "POST":
        return destinations_create(request)


def destinations_list(
    request,
    create_form: DestinationFormCreate,
    error_update_form: Optional[DestinationFormUpdate] = None,
) -> HttpResponse:
    update_forms = _get_destination_forms_grouped_by_media(request.user, error_update_form)
    context = {
        "form": create_form,
        "grouped_forms": update_forms,
    }
    return render(request, "htmx/destinations/destinations.html", context=context)


def _get_destination_forms_grouped_by_media(
    user, error_form: Optional[DestinationFormUpdate] = None
) -> dict[Media, list[DestinationFormUpdate]]:
    """Returns dict where key is media and value is list of tuples
    containing a destination and a pre-filled form for that destination."""
    grouped_destinations = {}
    media = Media.objects.all()
    for m in media:
        grouped_destinations[m] = []

    destinations = user.destinations.all()
    for destination in destinations:
        if error_form and destination.pk == error_form.instance.pk:
            form = error_form
        else:
            form = DestinationFormUpdate(
                instance=destination,
            )
        grouped_destinations[destination.media].append(form)

    return grouped_destinations


@require_POST
def destinations_create(request) -> HttpResponse:
    form = DestinationFormCreate(request.POST or None, request=request)

    if form.is_valid():
        form.save()
        return redirect("htmx:destinations")
    return destinations_list(request, form)


@require_POST
def destinations_update(request, pk: int) -> HttpResponse:
    destination = DestinationConfig.objects.get(pk=pk)
    form = DestinationFormUpdate(request.POST or None, instance=destination, request=request)
    if form.is_valid():
        form.save()
        return redirect("htmx:destinations")
    return destinations_list(request, DestinationFormCreate(), form)


@require_POST
def destinations_delete(request, pk: int) -> HttpResponse:
    destination = get_object_or_404(request.user.destinations.all(), pk=pk)

    try:
        medium = api_safely_get_medium_object(destination.media.slug)
        medium.raise_if_not_deletable(destination)
    except NotificationMedium.NotDeletableError as e:
        raise ValidationError(str(e))
    else:
        destination.delete()
        return redirect("htmx:destinations")
