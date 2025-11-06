from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    View,
)

from lead.forms import (
    LeadForm,
)
from client.models import (
    Client,
)
from team.models import (
    Team,
    Plan,
)

from lead.models import Lead


class LeadCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View for create new Lead instance

    <i>login required to show this page</i>
    """

    model = Lead
    template_name = "lead/add_lead.html"
    form_class = LeadForm
    success_url = reverse_lazy("lead:list")

    def get_success_message(self, cleaned_data):
        return f'The lead "{self.object.name}" have been successfully added'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # after the form valid check add
        # created_by value to the instance and save to db
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class LeadsListView(LoginRequiredMixin, ListView):
    """
    List view for list all leads created by requested user

    <i>login required to show this page</i>
    """

    model = Lead
    template_name = "lead/list_leads.html"
    context_object_name = "leads"

    # Modify default Lead.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            created_by=self.request.user,
            converted_to_client=False,
        )

        return queryset.order_by("-created_at")


class LeadDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for list lead details

    <i>login required to show this page</i>
    """

    model = Lead
    pk_url_kwarg = "id"
    context_object_name = "lead"
    template_name = "lead/detail_lead.html"

    def get_queryset(self):
        # return all Lead records related to the user
        # and filter if lead was not converted to client
        # (check LeadQuerySet to more info)
        return (
            super()
            .get_queryset()
            .get_for_user(self.request.user)
            .filter(converted_to_client=False)
        )


class LeadDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Lead
    pk_url_kwarg = "id"
    context_object_name = "lead"
    success_url = reverse_lazy("lead:list")

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    def get_success_message(self, cleaned_data):
        return 'The lead "%(name)s" have been successfully deleted' % {
            "name": self.object.name
        }


class LeadUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for edit lead created by requested user and
    having certain id
    """

    model = Lead
    form_class = LeadForm
    pk_url_kwarg = "id"
    template_name = "lead/edit_lead.html"

    def get_queryset(self):

        # choose the object only from
        # leads created by requested user
        return super().get_queryset().filter(created_by=self.request.user)

    def get_success_url(self):
        return reverse_lazy("lead:detail", kwargs={"id": self.object.id})

    def get_success_message(self, cleaned_data):
        return f'The lead "{self.object.name}" has been successfully updated.'

    def get_form_kwargs(self):

        # pass the user to the form
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ConvertToClientView(
    LoginRequiredMixin, SuccessMessageMixin, SingleObjectMixin, View
):
    """
    Convert lead into the client and add it into
    the database
    """

    model = Lead
    pk_url_kwarg = "id"

    def get_queryset(self):
        # filter leads that was created by user and
        # wasn't converted yet
        return (
            super()
            .get_queryset()
            .get_for_user(self.request.user)
            .filter(converted_to_client=False)
        )

    def get_success_message(self, cleaned_data):
        return f"The lead {self.object.name} was converted into a client"

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        return redirect("lead:detail", id=self.object.id)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        lead = self.object

        # checks if lead convertion will not cause the
        # client limit overflow
        client_count = Client.objects.filter(team=lead.team).count()
        plan_lim = lead.team.plan.max_clients

        # if actually cause send message error
        # and get back to the detailed page
        if client_count >= plan_lim:
            messages.error(
                request,
                f"The lead {lead.name} cant be converted into the client. "
                f"Plan was exceeded: {client_count} of {plan_lim} clients",
            )
            return redirect("lead:detail", id=lead.id)

        try:
            client = Client.objects.create(
                team=lead.team,
                name=lead.name,
                email=lead.email,
                description=lead.description,
                created_by=request.user,
            )
            lead.converted_to_client = True
            lead.save()

            messages.success(
                request,
                f'Lead "{lead.name}" was successfully converted to "{client.name}" client',
            )
            return redirect("client:detail", id=client.id)
        except Exception as e:
            messages.error(request, f"An error occured during conversion: {e}")
            return redirect("lead:detail", id=lead.id)
