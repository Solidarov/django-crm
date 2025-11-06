from django.urls import path

from lead.views import (
    add_lead,
    convert_to_client,
    LeadsListView,
    LeadDetailView,
    LeadDeleteView,
    LeadUpdateView,
)

app_name = "lead"

urlpatterns = [
    path("", LeadsListView.as_view(), name="list"),
    path("add/", add_lead, name="add"),
    path("<id>/", LeadDetailView.as_view(), name="detail"),
    path("<id>/delete/", LeadDeleteView.as_view(), name="delete"),
    path("<id>/edit/", LeadUpdateView.as_view(), name="edit"),
    path("<int:id>/convert/", convert_to_client, name="convert"),
]
