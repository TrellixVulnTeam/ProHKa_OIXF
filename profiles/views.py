from django.shortcuts import render

from administration.models import GlobalSetting

# Create your views here.


def indexProfile(request):
    setting = GlobalSetting.objects.get(status=True)
    context = {
        'setting': setting,
        'profile': True
    }
    return render(request, 'profiles/index.html', context)
