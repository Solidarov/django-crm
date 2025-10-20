from django.shortcuts import render


def index(request):
    """
    Renders the main page "core/index.html"
    """
    return render(request, 'core/index.html')

def about(request):
    """
    Render the about page "core/about.html" 
    """
    return render(request, 'core/about.html')