from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from team.models import Team
from team.forms import TeamForm


@login_required
def edit_team(request, id):
    """
    Edit team properties only when you're the owner
    """

    team = get_object_or_404(
        Team,
        created_by=request.user,
        pk=id,
    )
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()

            messages.success(request, "Team was successfully edited")

            return redirect("userprofile:myaccount")
    else:
        form = TeamForm(instance=team)

    context = {
        "team": team,
        "form": form,
    }

    return render(
        request,
        "team/edit_team.html",
        context=context,
    )
