from __future__ import annotations

from django.shortcuts import render

from django.http import HttpResponse

from .forms import DestinationForm


def destinations(request) -> HttpResponse:
    context = {
        "form": DestinationForm(),
    }
    return render(request, "htmx/destinations/destinations.html", context=context)
