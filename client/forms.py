from django import forms

from client.models import (
    Client,
)
from team.models import (
    Team,
)


class ClientForm(forms.ModelForm):
    """
    Form for Client model
    """

    class Meta:
        model = Client
        fields = (
            "name",
            "email",
            "description",
            "team",
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Retrive from database only teams created by requested user.
        # If no teams was found, return none queryset
        if "team" in self.fields:
            if user is not None:
                self.fields["team"].queryset = Team.objects.filter(members=user)
            else:
                self.fields["team"].queryset = Team.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        new_team = cleaned_data.get("team")

        # check if newly created instance
        if self.instance.pk:
            old_team = self.instance.team

            # if edited check if team was changed
            team_changed = old_team != new_team
            if not team_changed:
                return cleaned_data

        # if team was changed or newly created record
        # than check if client does not exceed team plan limit
        if new_team:
            client_count = Client.objects.filter(team=new_team).count()
            plan_lim = new_team.plan.max_clients

            # raise if exceeded
            if client_count >= plan_lim:
                raise forms.ValidationError(
                    f"The team plan for '{new_team.name}' was exceeded. "
                    f"It already has {client_count} of {plan_lim} leads. "
                )

        return cleaned_data
