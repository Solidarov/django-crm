from django.urls import path

from dashboard.views import (
    DashboardListView,
)

app_name = "dashboard"

urlpatterns = [
    path("", DashboardListView.as_view(), name="dashboard"),
]
