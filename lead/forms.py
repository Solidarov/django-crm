from django import forms

from lead.models import Lead

class AddLeadForm(forms.ModelForm):
    """
    Form for create new Lead model
    """
    class Meta:
        model = Lead
        fields = ('name', 'email', 'description', 'priority', 'status')