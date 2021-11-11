from administration.models import *
from django.shortcuts import render

# Create your views here.

def indexAbout(request):
    setting = GlobalSetting.objects.get(status=True)

    context = {
        'about':True,
        "setting":setting,
    }

    return render(request, 'aboutAndContact/about.html', context)


def indexContact(request):
    setting = GlobalSetting.objects.get(status=True)

    context = {
        'contact':True,
        "setting":setting,
    }

    return render(request, 'aboutAndContact/contact.html', context)