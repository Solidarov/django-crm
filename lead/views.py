from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from lead.forms import(AddLeadForm,)

from lead.models import Lead

@login_required
def add_lead(request):
    """
    View for create a new lead to the database
    <strong>(login required)</strong>
    """
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid:
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()

            messages.success(request, f"The lead \"{lead.name}\" have been successfully added")
            
            return redirect('lead:list')
    else:    
        form = AddLeadForm()

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

@login_required
def lead_detail(request, id):
    """
    View for list lead details created by <i>requested user</i> 
    and having certain <i>id</i>   
    """
    lead = get_object_or_404(Lead, created_by=request.user, pk=id)
    context = {
        'lead': lead,
    }

    return render(request, 'lead/detail_lead.html', context=context,)

@login_required
def delete_lead(request, id):
    """
    View for delete having certain <i>id</i> and 
    created by <i>requested user</i>     
    """
    lead = get_object_or_404(Lead, created_by=request.user, pk=id)
    lead.delete()

    messages.success(request, f"The lead \"{lead.name}\" have been successfully deleted")

    return redirect('lead:list')

@login_required
def edit_lead(request, id):
    """
    View for edit lead created by requested user and 
    having certain id
    """
    lead = get_object_or_404(Lead, created_by=request.user, pk=id,)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, f"Changes have been saved")
            return redirect('lead:detail', id=id)
    else:
        form = AddLeadForm(instance=lead)
    
    context = {
        'form': form,
    }
    return render(request, 'lead/edit_lead.html', context=context,)
