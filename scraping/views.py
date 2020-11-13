from django.shortcuts import render

from scraping.models import RealEstate


def home(request):
    qs = RealEstate.objects.filter(sent=False)
    return render(request, 'home.html', {'qs': qs})
