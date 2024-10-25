from django.urls import path

from . import views

app_name = "htmx"
urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("<int:pk>/", views.destinations_update, name="destinations-update"),
    path("<int:pk>/delete", views.destinations_delete, name="destinations-delete"),
]
