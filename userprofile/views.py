from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    FormView,
    TemplateView,
)

from userprofile.forms import CustomSignUpForm
from team.models import (
    Team,
)


class SignUpFormView(FormView):
    """
    View for creating <b>User</b> along
    with <b>UserProfile</b>, <b>Team</b>
    and <b>Basic Plan</b> if doesn't exist
    """

    form_class = CustomSignUpForm
    template_name = "userprofile/signup.html"
    success_url = reverse_lazy("dashboard:dashboard")

    def form_valid(self, form):
        user = form.save()

        login(self.request, user)

        messages.success(
            self.request,
            f"The user {user.username} was created successfully!",
        )

        return super().form_valid(form)


class MyAccountTemplateView(LoginRequiredMixin, TemplateView):
    """
    Renders the "My account" page with all
    teams user involved in
    """

    template_name = "userprofile/myaccount.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q_created_by = Q(created_by=self.request.user)
        q_member = Q(members=self.request.user)
        query = q_created_by | q_member
        teams = Team.objects.filter(query).distinct()
        context["teams"] = teams

        return context
