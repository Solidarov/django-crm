from django.urls import path

import userprofile.views as view

app_name = 'userprofile'

urlpatterns = [
    path('sign-up/', view.signup, name='signup'),
]