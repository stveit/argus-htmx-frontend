from __future__ import annotations

from django.shortcuts import redirect, render

from django.http import HttpResponse

from django.views.decorators.http import require_GET, require_POST

from argus.notificationprofile.models import DestinationConfig, Media
from argus.notificationprofile.media import api_safely_get_medium_object

from .forms import DestinationForm


@require_GET
def destinations(request) -> HttpResponse:
    destinations = _get_destinations_and_forms_grouped_by_media(request.user)
    context = {
        "form": DestinationForm(),
        "grouped_destinations": destinations,
    }
    return render(request, "htmx/destinations/destinations.html", context=context)


def _get_destinations_and_forms_grouped_by_media(user) -> dict[Media, list[DestinationConfig]]:
    """Returns dict where key is media and value is list of tuples
    containing a destination and a pre-filled form for that destination."""
    grouped_destinations = {}

    media = Media.objects.all()
    for m in media:
        grouped_destinations[m] = []

    destinations = user.destinations.all()
    for destination in destinations:
        form = DestinationForm(
            initial={
                "label": destination.label,
                "media": destination.media.slug,
                "value": destination.settings.get("email_address", ""),
            }
        )
        form.fields["media"].widget.attrs["hidden"] = True
        grouped_destinations[destination.media].append((destination, form))

    return grouped_destinations


@require_POST
def destinations_create(request) -> HttpResponse:
    form = DestinationForm(request.POST or None)
    if form.is_valid():
        media = Media.objects.get(slug=form.cleaned_data["media"])
        medium = api_safely_get_medium_object(media.slug)
        # e.g. "email_address", "phone_number" etc.
        settings_key = medium.MEDIA_JSON_SCHEMA["required"][0]
        destination = DestinationConfig.objects.create(
            user=request.user,
            media=media,
            label=form.cleaned_data.get("label", ""),
            settings={settings_key: form.cleaned_data["value"]},
        )
        destination.save()
    return redirect("htmx:destinations")
