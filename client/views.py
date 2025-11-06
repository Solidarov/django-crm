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
    DeleteView,
    UpdateView,
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
    template_name = "client/client_form.html"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Create new client"
        context["button_name"] = "Create"
        return context


class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    View for deleting a client created by requested user
    and having a certain id
    """

    model = Client
    success_url = reverse_lazy("client:list")
    pk_url_kwarg = "id"
    context_object_name = "client"

    def get_success_message(self, cleaned_data):
        return f'The client "{self.object.name}" was deleted successfully'

    def get_queryset(self):
        # get queryset created by current user
        return super().get_queryset().filter(created_by=self.request.user)


class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for edit client, created by requested user and
    having a certain id
    """

    model = Client
    form_class = ClientForm
    pk_url_kwarg = "id"
    template_name = "client/client_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy("client:detail", kwargs={"id": self.object.id})

    def get_success_message(self, cleaned_data):
        return f'The client "{self.object.name}" has been successfully updated.'

    def get_context_data(self, **kwargs):
        # pass additional data to client_form
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'Edit "{self.object.name}"'
        context["button_name"] = "Edit"
        return context
