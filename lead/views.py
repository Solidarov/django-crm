from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from lead import views, forms
from lead.models import Lead

@login_required
def add_lead(request):
    """
    View for create a new lead to the database
    <strong>(login required)</strong>
    """
    if request.method == 'POST':
        form = forms.AddLeadForm(request.POST)
        if form.is_valid:
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            return redirect('dashboard:dashboard')
    else:    
        form = forms.AddLeadForm()

    context = {
        'form': form,
    }
    return render(request, 'lead/add_lead.html', context=context)

@login_required
def list_leads(request):
    """
    View for list all leads created by requested user
    """
    leads = Lead.objects.filter(created_by=request.user)
    context = {
        'leads': leads,
    }
    return render(request, 'lead/list_leads.html', context=context)