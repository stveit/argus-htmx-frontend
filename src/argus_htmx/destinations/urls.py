from django.urls import path

from . import views

app_name = "htmx"
urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("create_destination/", views.destinations_create, name="destinations-create"),
    path("<int:pk>/", views.destinations_update, name="destinations-update"),
    path("delete_destination/<int:pk>/", views.destinations_delete, name="destinations-delete"),
]
