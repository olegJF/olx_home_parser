from datetime import datetime

from django.shortcuts import render, get_object_or_404

from scraping.models import RealEstate


def home(request):
    today = datetime.today()
    qs = RealEstate.objects.all().order_by('-updated')  # filter(updated=today)
    return render(request, 'home.html', {'qs': qs})


def detail(request, id):
    obj = get_object_or_404(RealEstate, id=id)
    return render(request, 'detail.html', {'object': obj})
