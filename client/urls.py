from django.urls import path

from client.views import (
    add_client,
    delete_client,
    edit_client,
    ClientListView,
    ClientDetailView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("<id>/", ClientDetailView.as_view(), name="detail"),
    path("add/", add_client, name="add"),
    path("<int:id>/delete/", delete_client, name="delete"),
    path("<int:id>/edit/", edit_client, name="edit"),
]
