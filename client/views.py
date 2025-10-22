from django.contrib.auth.decorators import login_required
from django.shortcuts import (render,
                              get_object_or_404,)

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

@login_required
def detail_client(request, id):
    """
    View for list client details created by <i>requested user</i> 
    and having certain <i>id</i>
    """
    client = get_object_or_404(Client, created_by=request.user, pk=id)
    context = {
        'client': client,
    }
    return render(request, 'client/detail_client.html', context=context)