from django.urls import path

from lead.views import (
    list_leads,
    add_lead,
    lead_detail,
    delete_lead,
    edit_lead,
    convert_to_client,
)

app_name = "lead"

urlpatterns = [
    path("", list_leads, name="list"),
    path("add/", add_lead, name="add"),
    path("<int:id>/", lead_detail, name="detail"),
    path("<int:id>/delete/", delete_lead, name="delete"),
    path("<int:id>/edit/", edit_lead, name="edit"),
    path("<int:id>/convert/", convert_to_client, name="convert"),
]
