from django.urls import path

from client.views import (
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientDeleteView,
    ClientUpdateView,
)

app_name = "client"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("add/", ClientCreateView.as_view(), name="add"),
    path("<int:id>/", ClientDetailView.as_view(), name="detail"),
    path("<int:id>/delete/", ClientDeleteView.as_view(), name="delete"),
    path("<int:id>/edit/", ClientUpdateView.as_view(), name="edit"),
]
