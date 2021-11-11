from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def loginUser(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/custom/home/")
        else:
            return redirect("auth:login")
    context = {}
    return render(request, "authentication/index.html", context)


def logoutUser(request):
    print('access the method')
    logout(request)
    return redirect("auth:login")
    