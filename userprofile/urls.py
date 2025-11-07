from django.urls import path
import django.contrib.auth.views as views

from userprofile.views import (
    user_logout,
    myaccount,
    SignUpFormView,
)

app_name = "userprofile"

urlpatterns = [
    path("sign-up/", SignUpFormView.as_view(), name="signup"),
    path(
        "log-in/",
        views.LoginView.as_view(template_name="userprofile/login.html"),
        name="login",
    ),
    path("log-out/", user_logout, name="logout"),
    path("my-account/", myaccount, name="myaccount"),
]
