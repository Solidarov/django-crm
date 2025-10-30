from django import forms

from client.models import (
    Client,
)
from team.models import (
    Team,
)


class AddClientForm(forms.ModelForm):
    """
    Form for adding a new client instance to database
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
