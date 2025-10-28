from django.urls import path

from team.views import edit_team

app_name = "team"

urlpatterns = [
    path("<int:id>/edit/", edit_team, name="edit"),
]
