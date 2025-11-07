from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from team.models import (
    Team,
    Plan,
)


class CustomSignUpForm(UserCreationForm):
    """
    Custom creation form for User
    """

    # overwrite the UserCreationForm email field
    # basically add '(optional)' clause
    email = forms.EmailField(label="Email address (optional)", required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)

    # if something goes wrong cancel all changes
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit)

        # check if basic plan exist
        # if not then create new with default values
        basic_plan, _ = Plan.objects.get_or_create(
            pk=1,
            defaults={"name": "Basic", "price": 10, "max_leads": 2, "max_clients": 2},
        )

        # create new team for the new user
        # and add him to members
        team = Team.objects.create(
            name=f"{user.username}_team",
            created_by=user,
            plan=basic_plan,
        )
        team.members.set([user])

        UserProfile.objects.create(user=user)

        return user
