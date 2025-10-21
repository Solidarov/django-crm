from django.urls import path

import lead.views as lead_view

app_name = 'lead'

urlpatterns = [
    
    path('', lead_view.list_leads, name='list'),
    path('add/', lead_view.add_lead, name='add'),
    path('<int:id>/', lead_view.lead_detail, name='detail'),
]