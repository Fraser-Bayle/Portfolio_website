from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def technologies(request):
    return render(request, 'pages/technologies.html')

def easter_egg(request):
    return render(request, 'pages/easter_egg.html')