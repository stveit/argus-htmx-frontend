from __future__ import annotations

from django.shortcuts import render

from django.http import HttpResponse


def destinations(request) -> HttpResponse:
    context = {}
    return render(request, "htmx/destinations/destinations.html", context=context)
