from django.urls import path

from . import views

app_name = "destinations"
urlpatterns = [
    path("", views.destinations, name="destinations"),
]
