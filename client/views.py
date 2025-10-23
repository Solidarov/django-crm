from django.contrib.auth.decorators import login_required
from django.shortcuts import (render,
                              get_object_or_404,
                              redirect,)
from django.contrib import messages

from client.models import (Client,)
from client.forms import (AddClientForm,)

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

@login_required
def add_client(request):
    """
    View for adding a new client
    """
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(
                request, 
                'The new client have been created',
                )
            
            return redirect('client:list')
    else:
        form = AddClientForm()

    context = {
        'form': form,
    }
    return render(
        request, 
        'client/add_client.html', 
        context=context,
        )

@login_required
def delete_client(request, id):
    client = get_object_or_404(Client, created_by=request.user, pk=id)
    client.delete()

    messages.success(
        request,
        f'The {client.name} client was successfully deleted',
    )

    return redirect('client:list')

@login_required
def edit_client(request, id):
    """
    View for edit client, created by requested user and 
    having a certain id
    """
    client = get_object_or_404(Client, created_by=request.user, pk=id)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

            messages.success(
                request,
                'The client was successfully updated',
            )

            return redirect('client:detail', id=id)
        
    else:
        form = AddClientForm(instance=client)

    context = {
        'form': form,
    }
    return render(
        request, 
        'client/edit_client.html', 
        context=context,
        )