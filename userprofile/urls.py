from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

from userprofile.views import (
    myaccount,
    SignUpFormView,
)

app_name = "userprofile"

urlpatterns = [
    path("sign-up/", SignUpFormView.as_view(), name="signup"),
    path(
        "log-in/",
        LoginView.as_view(template_name="userprofile/login.html"),
        name="login",
    ),
    path("my-account/", myaccount, name="myaccount"),
    # actual logout logic
    path(
        "logout/",
        LogoutView.as_view(
            next_page="userprofile:logout_done",
        ),
        name="logout",
    ),
    # conformation of successfull logout
    path(
        "logout/done",
        TemplateView.as_view(
            template_name="userprofile/logout_done.html",
        ),
        name="logout_done",
    ),
]
