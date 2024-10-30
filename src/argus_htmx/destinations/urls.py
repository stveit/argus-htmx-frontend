from django.urls import path

from .views import destinations, destinations_delete

app_name = "htmx"
urlpatterns = [
    path("", destinations, name="destinations"),
    path("<int:pk>/delete", destinations_delete, name="destinations-delete"),
]
