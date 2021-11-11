from django.urls import path, include
from authentication.views import *

urlpatterns = [
    path("api/", include("authentication.api.urls", namespace="apiCustom")),
    path("login/", loginUser, name="login"),
    path("logout/", logoutUser, name="logout"),
]
app_name="authentication"