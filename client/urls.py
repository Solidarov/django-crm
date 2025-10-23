from django.urls import path

from client.views import (
    list_clients,
    detail_client,
    add_client,
    delete_client,
    edit_client,
)

app_name = "client"

urlpatterns = [
    path("", list_clients, name="list"),
    path("<int:id>/", detail_client, name="detail"),
    path("add/", add_client, name="add"),
    path("<int:id>/delete/", delete_client, name="delete"),
    path("<int:id>/edit/", edit_client, name="edit"),
]
