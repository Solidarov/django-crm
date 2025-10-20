from django.shortcuts import render


def index(request):
    """
    Renders the main page "core/index.html"
    """
    return render(request, 'core/index.html')