from django.urls import path

from .views import destinations

app_name = "htmx"
urlpatterns = [
    path("", destinations, name="destinations"),
]
