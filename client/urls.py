from django.urls import path

from client.views import (list_clients,)

app_name = "client"

urlpatterns = [
    path('', list_clients, name='list'),
]