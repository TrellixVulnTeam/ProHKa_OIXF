from django.urls import path
from authentication.api.views import *


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("get-all-user/", UserAPIView.as_view(), name="showUser"),
]
app_name = "authApi"
