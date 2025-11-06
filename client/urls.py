from django.urls import path

from client.views import (
    edit_client,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientDeleteView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("add/", ClientCreateView.as_view(), name="add"),
    path("<int:id>/", ClientDetailView.as_view(), name="detail"),
    path("<int:id>/delete/", ClientDeleteView.as_view(), name="delete"),
    path("<int:id>/edit/", edit_client, name="edit"),
]
