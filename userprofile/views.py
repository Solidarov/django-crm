from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from userprofile.models import UserProfile

def signup(request):
    """
    View for creating <b>User</b> along with <b>UserProfile</b>
    \nRender <i>'userprofile/signup.html'</i> template 
with <i>UserCreationForm</i> as 'form'.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            UserProfile.objects.create(user=user)

            return redirect('core:index')
    else:
        
        form = UserCreationForm()

    return render(request, 
                  'userprofile/signup.html', 
                  {
                    'form': form,  
                  },)