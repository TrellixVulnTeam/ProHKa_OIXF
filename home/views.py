from django.shortcuts import render
from administration.models import *

# Create your views here.


def index(request):
    users = UserRegistration.objects.filter(status=True).order_by('updated')[:4]
    slides = Slides.objects.all().order_by('-updated')[:3]
    setting = GlobalSetting.objects.get(status=True)
    context = {
        'home':True,
        "users":users,
        "slides":slides,
        "setting":setting,
    }

    return render(request, 'home/index.html', context)