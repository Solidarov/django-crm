from django import forms

from lead.models import (
    Lead,
)

from team.models import (
    Team,
)


class LeadForm(forms.ModelForm):
    """
    Form for Lead model
    """

    class Meta:
        model = Lead
        fields = (
            "name",
            "email",
            "description",
            "priority",
            "status",
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

        old_team = None
        new_team = cleaned_data.get("team")

        # check if instance is newly created
        # if not check if team was changed
        if self.instance.pk:
            old_team = self.instance.team

            # check if team was not changed
            team_changed = new_team != old_team
            if not team_changed:
                return cleaned_data

        # checks if new/edited lead dont exceed
        # the team plan limit
        if new_team:
            lead_counts = Lead.objects.filter(
                team=new_team, converted_to_client=False
            ).count()
            plan_lim = new_team.plan.max_leads

            # if exceed raise the form error
            if lead_counts >= plan_lim:
                raise forms.ValidationError(
                    f"The team plan for '{new_team.name}' was exceeded. "
                    f"It already has {lead_counts} of {plan_lim} leads. "
                )

        return cleaned_data
