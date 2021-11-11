from django.urls import path, include
from profiles.views import *
# from administration.views import *

urlpatterns = [
    path("api/", include("profiles.api.urls", namespace="apiProfiles")),
    path("", indexProfile, name="profil"),
]
app_name = "apiProfile"
