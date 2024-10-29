from __future__ import annotations

from django.shortcuts import redirect, render, get_object_or_404

from django.http import HttpResponse

from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework.exceptions import ValidationError

from argus.notificationprofile.models import DestinationConfig, Media
from argus.notificationprofile.media import api_safely_get_medium_object
from argus.notificationprofile.serializers import RequestDestinationConfigSerializer
from argus.notificationprofile.media.base import NotificationMedium

from .forms import DestinationFormCreate, DestinationFormUpdate

from .utils import _get_settings_key_for_media


@require_http_methods(["GET", "POST"])
def destinations(request) -> HttpResponse:
    if request.method == "GET":
        return destinations_list(request)
    elif request.method == "POST":
        return destinations_create(request)


@require_GET
def destinations_list(request) -> HttpResponse:
    forms = _get_destination_forms_grouped_by_media(request.user)
    context = {
        "form": DestinationFormCreate(),
        "grouped_forms": forms,
    }
    return render(request, "htmx/destinations/destinations.html", context=context)


def _get_destination_forms_grouped_by_media(user) -> dict[Media, list[DestinationFormUpdate]]:
    """Returns dict where key is media and value is list of tuples
    containing a destination and a pre-filled form for that destination."""
    grouped_destinations = {}
    media = Media.objects.all()
    for m in media:
        grouped_destinations[m] = []

    destinations = user.destinations.all()
    for destination in destinations:
        form = DestinationFormUpdate(
            instance=destination,
        )
        grouped_destinations[destination.media].append(form)

    return grouped_destinations


@require_POST
def destinations_create(request) -> HttpResponse:
    form = DestinationFormCreate(request.POST or None)
    if form.is_valid():
        serializer = RequestDestinationConfigSerializer(
            data={
                "media": form.cleaned_data["media"],
                "label": form.cleaned_data.get("label", ""),
                "settings": form.cleaned_data["settings"],
            },
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

    return redirect("htmx:destinations")


@require_POST
def destinations_update(request, pk: int) -> HttpResponse:
    form = DestinationFormUpdate(request.POST or None)
    if form.is_valid():
        destination = DestinationConfig.objects.get(pk=pk)
        settings_key = _get_settings_key_for_media(destination.media)
        data = {}
        if "label" in form.cleaned_data:
            label = form.cleaned_data["label"]
            if label != destination.label:
                data["label"] = label
        settings = form.cleaned_data["settings"]
        # If email, phone number etc. is different in the form than in the database
        if settings.get(settings_key) != destination.settings.get(settings_key):
            data["settings"] = settings

        serializer = RequestDestinationConfigSerializer(
            destination,
            data=data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

    return redirect("htmx:destinations")


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
