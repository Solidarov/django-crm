from django import forms

from lead.models import (
    Lead,
)

from team.models import (
    Team,
)


class AddLeadForm(forms.ModelForm):
    """
    Form for create new Lead model
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
