from django.urls import path
from gallery.views import *
from administration.views import *

urlpatterns = [
    path("gallery/", indexGallery, name="indexGallery"),
    path("gallery/<int:id>/", showSingleUser, name="singleUser"),
    # path("about/", aboutUs, name="customAbout"),
]
app_name="apiGallery"