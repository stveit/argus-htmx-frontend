from django.urls import path

from . import views

app_name = "htmx"
urlpatterns = [
    path("", views.destinations, name="destinations"),
]
