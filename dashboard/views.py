from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from client.models import Client
from lead.models import Lead


@login_required
def dashboard(request):
    """
    View for dashboard pages with all client and leads realated to the requested user
    """

    leads = Lead.objects.get_for_user(request.user).filter(converted_to_client=False)
    clients = Client.objects.get_for_user(request.user)

    context = {
        "leads": leads,
        "clients": clients,
    }
    return render(
        request,
        "dashboard/dashboard.html",
        context=context,
    )
