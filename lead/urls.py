from django.urls import path

import lead.views as lead_view

app_name = 'lead'

urlpatterns = [

    path('add-lead/', lead_view.add_lead, name='add_lead')
]