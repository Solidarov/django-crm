from django import forms

from client.models import (Client,)

class AddClientForm(forms.ModelForm):
    """
    Form for adding a new client instance to database
    """
    class Meta:
        model = Client    
        fields = ('name', 'email', 'description')
