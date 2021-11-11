from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required(login_url="/auth/login/")
def homeCustom(request):
    print('thr user is ', request.user)
    context = {
        'custom':True
    }

    return render(request, 'admin/custom.html', context)

@login_required(login_url="/auth/login/")
def aboutUs(request):
    context = {
        'global':True
    }

    return render(request, 'admin/global.html', context)

@login_required(login_url="/auth/login/")
def slide(request):
    context = {
        'global':True,
    }

    return render(request, 'admin/global.html', context)

@login_required(login_url="/auth/login/")
def getOffer(request):
    context = {
        'command':True
    }

    return render(request, "admin/command.html", context)

@login_required(login_url="/auth/login/")
def getAllMsg(request):
    context = {
        'command':True
    }
    return render (request, 'admin/allMsg.html', context)