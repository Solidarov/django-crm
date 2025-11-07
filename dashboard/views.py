from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from client.models import Client
from lead.models import Lead


class DashboardListView(LoginRequiredMixin, ListView):
    """
    View for dashboard pages with all client and leads realated to the requested user
    """

    model = Lead
    template_name = "dashboard/dashboard.html"
    context_object_name = "leads"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.get_for_user(self.request.user).filter(converted_to_client=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.get_for_user(self.request.user)
        return context
