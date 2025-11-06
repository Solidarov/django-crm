from django.urls import path

from client.views import (
    delete_client,
    edit_client,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("add/", ClientCreateView.as_view(), name="add"),
    path("<int:id>/", ClientDetailView.as_view(), name="detail"),
    path("<int:id>/delete/", delete_client, name="delete"),
    path("<int:id>/edit/", edit_client, name="edit"),
]
