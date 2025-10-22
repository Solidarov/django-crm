from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from client.models import (Client,)

@login_required
def list_clients(request):
    """
    View for listing the clients created by requested user
    """
    clients = Client.objects.filter(created_by=request.user)
    context = {
        'clients': clients,
    }
    return render(request, 'client/list_clients.html', context=context)