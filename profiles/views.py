from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from administration.models import GlobalSetting, UserRegistration
from authentication.models import User

# Create your views here.


@login_required(login_url='/auth/login/')
def indexProfile(request):
    if request.user.is_authenticated:
        id = request.user.id
        profiles = UserRegistration.objects.filter(owner_id=int(id))
        user = User.objects.get(id=int(id))
        setting = GlobalSetting.objects.get(status=True)
        context = {
            'setting': setting,
            'profiles': profiles,
            'profile': True
        }
        return render(request, 'profiles/index.html', context)
    else:
        context = {}
        return render(request, 'gallery/erroPage.html', context)
