from __future__ import annotations

from django.shortcuts import render

from django.http import HttpResponse

from django.views.decorators.http import require_GET

from argus.notificationprofile.models import DestinationConfig, Media

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
