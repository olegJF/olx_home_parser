from datetime import datetime

from django.shortcuts import render

from scraping.models import RealEstate


def home(request):
    today = datetime.today()
    qs = RealEstate.objects.filter(updated=today)
    return render(request, 'home.html', {'qs': qs})
