from django.urls import path
import django.contrib.auth.views as views

import userprofile.views as user_views

app_name = "userprofile"

urlpatterns = [
    path("sign-up/", user_views.signup, name="signup"),
    path(
        "log-in/",
        views.LoginView.as_view(template_name="userprofile/login.html"),
        name="login",
    ),
    path("log-out/", user_views.user_logout, name="logout"),
]
