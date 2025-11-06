from django.urls import path

from client.views import (
    detail_client,
    add_client,
    delete_client,
    edit_client,
    ClientListView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("<int:id>/", detail_client, name="detail"),
    path("add/", add_client, name="add"),
    path("<int:id>/delete/", delete_client, name="delete"),
    path("<int:id>/edit/", edit_client, name="edit"),
]
