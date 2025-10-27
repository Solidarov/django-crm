from django import forms

from team.models import Team


class TeamForm(forms.ModelForm):
    """
    Form based on Team model

    Include fields:
        - name
        - members
    """

    class Meta:
        model = Team
        fields = ("name", "members")
