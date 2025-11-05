from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
)

from lead.forms import (
    AddLeadForm,
)
from client.models import (
    Client,
)
from team.models import (
    Team,
    Plan,
)

from lead.models import Lead


@login_required
def add_lead(request):
    """
    View for create a new lead to the database
    <strong>(login required)</strong>
    """
    if request.method == "POST":
        form = AddLeadForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            # Checks if plan limit is not exceeded
            team = form.cleaned_data.get("team")
            team_count = Lead.objects.filter(
                team=team, converted_to_client=False
            ).count()
            plan_lim = team.plan.max_leads

            if team_count >= plan_lim:
                messages.error(request, f"The plan was exceeded")
                context = {
                    "form": form,
                }
                return render(request, "lead/add_lead.html", context=context)

            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            messages.success(
                request, f'The lead "{lead.name}" have been successfully added'
            )

            return redirect("lead:list")
    else:
        form = AddLeadForm(
            user=request.user,
        )

    context = {
        "form": form,
    }
    return render(request, "lead/add_lead.html", context=context)


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


@login_required
def delete_lead(request, id):
    """
    View for delete having certain <i>id</i> and
    created by <i>requested user</i>
    """
    lead = get_object_or_404(Lead, created_by=request.user, pk=id)
    lead.delete()

    messages.success(request, f'The lead "{lead.name}" have been successfully deleted')

    return redirect("lead:list")


@login_required
def edit_lead(request, id):
    """
    View for edit lead created by requested user and
    having certain id
    """
    lead = get_object_or_404(
        Lead,
        created_by=request.user,
        pk=id,
    )

    if request.method == "POST":
        form = AddLeadForm(
            request.POST,
            instance=lead,
            user=request.user,
        )
        if form.is_valid():

            # Checks if plan limit is not exceeded

            change_team = "team" in form.changed_data  # checks if team was changed

            team = form.cleaned_data.get("team")
            lead_counts = Lead.objects.filter(
                team=team, converted_to_client=False
            ).count()
            plan_lim = team.plan.max_leads

            # checks if limit was exceeded and if team was changed
            if lead_counts >= plan_lim and change_team:
                messages.error(request, f"The team plan was exceeded")
                context = {
                    "form": form,
                }
                return render(request, "lead/edit_lead.html", context=context)

            form.save()
            messages.success(request, f"Changes have been saved")
            return redirect("lead:detail", id=id)
    else:
        form = AddLeadForm(
            instance=lead,
            user=request.user,
        )

    context = {
        "form": form,
    }
    return render(
        request,
        "lead/edit_lead.html",
        context=context,
    )


@login_required
def convert_to_client(request, id):
    """
    Convert lead into the client and add it into the database
    """
    leads = Lead.objects.get_for_user(
        request.user
    )  # get all clients related to the request user
    lead = get_object_or_404(
        leads,
        converted_to_client=False,
        pk=id,
    )

    # Check if plan was not exceeded
    team_count = Client.objects.filter(team=lead.team).count()
    plan_lim = lead.team.plan.max_clients
    if team_count >= plan_lim:
        messages.error(
            request,
            f"The team plan was exceeded",
        )

        return redirect("lead:detail", lead.id)

    Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        created_by=lead.created_by,
        team=lead.team,
    )

    lead.converted_to_client = True
    lead.save()

    messages.success(request, "The lead was converted into a client")
    return redirect("lead:list")
