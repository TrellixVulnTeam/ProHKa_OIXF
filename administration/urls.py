from django.urls import path, include
from administration.views import *

urlpatterns = [
    path("api/", include("administration.api.urls", namespace="apiCustom")),
    path("home/", homeCustom, name="customHome"),
    path("slide/", slide, name="customSlide"),
    path("about/", aboutUs, name="customAbout"),
    path("get-command/", getOffer, name="getCommand"),
    path("retrieve-message/", getAllMsg, name="getMsg"),
]
app_name="apiAdministation"