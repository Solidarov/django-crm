from django.urls import path

from client.views import (list_clients,
                          detail_client,
                          add_client,)

app_name = "client"

urlpatterns = [
    path('', list_clients, name='list'),
    path('<int:id>/', detail_client, name='detail'),
    path('add/', add_client, name='add'),
]