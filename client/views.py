from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
)

from client.models import (
    Client,
)
from team.models import (
    Plan,
)
from client.forms import (
    AddClientForm,
)


class ClientListView(LoginRequiredMixin, ListView):
    """
    View for listing the clients created by requested user
    """

    model = Client
    template_name = "client/list_clients.html"
    context_object_name = "clients"

    # get all clients created by user
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(created_by=self.request.user)
            .order_by("-created_at")
        )


@login_required
def detail_client(request, id):
    """
    View for list client details
    """
    clients = Client.objects.get_for_user(
        request.user,
    )  # get clients related to request user
    client = get_object_or_404(
        clients,
        pk=id,
    )
    context = {
        "client": client,
    }
    return render(request, "client/detail_client.html", context=context)


@login_required
def add_client(request):
    """
    View for adding a new client
    """
    if request.method == "POST":
        form = AddClientForm(request.POST, user=request.user)

        if form.is_valid():

            # Check if plan limit is not exceeded
            team = form.cleaned_data.get("team")
            client_count = Client.objects.filter(team=team).count()
            plan_lim = team.plan.max_clients

            if client_count >= plan_lim:
                messages.error(request, f"The plan was exceeded")
                context = {
                    "form": form,
                }
                return render(request, "client/add_client.html", context=context)

            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(
                request,
                "The new client has been created",
            )

            return redirect("client:list")
    else:
        form = AddClientForm(user=request.user)

    context = {
        "form": form,
    }
    return render(
        request,
        "client/add_client.html",
        context=context,
    )


@login_required
def delete_client(request, id):
    """
    View for deleting a client created by requested user
    and having a certain id
    """
    client = get_object_or_404(
        Client,
        created_by=request.user,
        pk=id,
    )
    client.delete()

    messages.success(
        request,
        f"The {client.name} client was successfully deleted",
    )

    return redirect("client:list")


@login_required
def edit_client(request, id):
    """
    View for edit client, created by requested user and
    having a certain id
    """
    client = get_object_or_404(Client, created_by=request.user, pk=id)

    if request.method == "POST":
        form = AddClientForm(request.POST, instance=client, user=request.user)
        if form.is_valid():

            changed_team = "team" in form.changed_data  # checks if team was changed
            # Check if plan limit is not exceeded
            team = form.cleaned_data.get("team")
            client_count = Client.objects.filter(team=team).count()
            plan_lim = team.plan.max_clients

            if client_count >= plan_lim and changed_team:
                messages.error(request, f"The plan was exceeded")
                context = {
                    "form": form,
                }
                return render(request, "client/edit_client.html", context=context)

            form.save()

            messages.success(
                request,
                "The client was successfully updated",
            )

            return redirect("client:detail", id=id)

    else:
        form = AddClientForm(instance=client, user=request.user)

    context = {
        "form": form,
    }
    return render(
        request,
        "client/edit_client.html",
        context=context,
    )
