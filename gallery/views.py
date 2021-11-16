from django.shortcuts import render
from administration.models import *
import json
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


def indexGallery(request):
    users = UserRegistration.objects.filter(status=True).order_by('-updated')
    setting = GlobalSetting.objects.get(status=True)

    context = {
        'users': users,
        'gallery': True,
        'setting': setting,
    }

    return render(request, 'gallery/index.html', context)


@login_required(login_url='/auth/login/')
def showSingleUser(request, id):
    errors = {}
    setting = ''
    otherImg = []
    if request.user.is_authenticated:
        user = UserRegistration.objects.get(id=id)
        # print("qwerty qwerty", user)
        setting = GlobalSetting.objects.get(status=True)
        if request.user.id and user.user_id and (int(request.user.id) == int(user.user_id)):
            if user.saveOtherImg:
                otherImg = json.loads(user.saveOtherImg)
            else:
                otherImg = []

        else:
            errors['user'] = "Vous n'êtes pas autorisés à ouvrir ce lien"
        if len(errors) == 0:
            context = {
                'user': user,
                'otherImg': otherImg,
                'setting': setting
            }
            return render(request, 'gallery/single.html', context)
        else:
            context = {
                'setting': setting,
                "errors": errors
            }
            return render(request, 'gallery/erroPage.html', context)
