from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def features(request):
    return render(request, 'how_it_works.html')
