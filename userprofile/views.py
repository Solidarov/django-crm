from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from userprofile.models import UserProfile
from team.models import Team


def signup(request):
    """
        View for creating <b>User</b> along with <b>UserProfile</b>
        \nRender <i>'userprofile/signup.html'</i> template
    with <i>UserCreationForm</i> as 'form'.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user)

            team = Team.objects.create(
                name=f"{user.username}_team",
                created_by=user,
            )
            team.members.add(user)
            team.save()

            return redirect("userprofile:login")
    else:

        form = UserCreationForm()

    return render(
        request,
        "userprofile/signup.html",
        {
            "form": form,
        },
    )


@login_required
def user_logout(request):
    """
    View for logout requested user
    """
    logout(request)
    return render(request, "userprofile/logout.html")


@login_required
def myaccount(request):
    """
    Renders the "My account" page with all
    teams user involved in
    """

    q_created_by = Q(created_by=request.user)
    q_member = Q(members=request.user)
    query = q_created_by | q_member

    teams = Team.objects.filter(query).distinct()

    context = {
        "teams": teams,
    }
    return render(
        request,
        "userprofile/myaccount.html",
        context=context,
    )
