from django.urls import path

from .views import destinations, destinations_delete, destinations_update

app_name = "htmx"
urlpatterns = [
    path("", destinations, name="destinations"),
    path("<int:pk>/delete", destinations_delete, name="destinations-delete"),
    path("<int:pk>/", destinations_update, name="destinations-update"),
]
