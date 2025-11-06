from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)

from client.models import (
    Client,
)
from team.models import (
    Plan,
)
from client.forms import (
    ClientForm,
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


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    View for list client details
    """

    model = Client
    pk_url_kwarg = "id"
    context_object_name = "client"
    template_name = "client/detail_client.html"

    # get clients related to request user
    def get_queryset(self):
        return super().get_queryset().get_for_user(self.request.user)


class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for adding a new client
    """

    model = Client
    form_class = ClientForm
    template_name = "client/add_client.html"
    success_url = reverse_lazy("client:list")

    def get_success_message(self, cleaned_data):
        return f'The client "{self.object.name}" has been created'

    def form_valid(self, form):
        # add value to created_by field and save form
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # specify user variable for the form init
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


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
        form = ClientForm(request.POST, instance=client, user=request.user)
        if form.is_valid():

            form.save()

            messages.success(
                request,
                "The client was successfully updated",
            )

            return redirect("client:detail", id=id)

    else:
        form = ClientForm(instance=client, user=request.user)

    context = {
        "form": form,
    }
    return render(
        request,
        "client/edit_client.html",
        context=context,
    )
