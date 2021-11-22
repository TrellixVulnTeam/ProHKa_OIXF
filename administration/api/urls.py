from django.urls import path
from administration.api.views import *


urlpatterns = [
    path("show-all-profiles/", ProfileListing.as_view(), name="showAllProfiles"),
    path("show-profile/", ProfileRegistrationAPIView.as_view(), name="showProfile"),
    path("add-profile/", ProfileRegistrationAPIView.as_view(), name="addProfile"),
    path("add-evaluation/", EvaluateAPIView.as_view(), name="addEvaluate"),
    path("retrieve-setting/", GlobalSettingAPIView.as_view(), name="retrieveSetting"),
    path("add-setting/", GlobalSettingAPIView.as_view(), name="addSetting"),
    # path("receive-mail/", ReceiveCommandAPIView.as_view(), name="emailRecived"),
    # path("get-all-command/", ReceiveCommandAPIView.as_view(), name="getAllCommand"),
    # path("edit-status-command/<int:pk>/",
    #      CommandEditAPIView.as_view(), name="editCommand"),
    path("retrieve-message/", ContactUsAPIView.as_view(), name="retrieveMsg"),
    path("contact-us/", ContactUsAPIView.as_view(), name="writeMsg"),
    path("edit-message/<int:id>/", MessageEditAPIView.as_view(), name="editMsg"),
    path("edit-profile/<int:pk>/", ProfileEditAPIView.as_view(), name="editProfile"),
    path("send-proposition/", SendProposition.as_view(), name="proposition"),
    path("choice-client/", ChoiceCLient.as_view(), name="proposition"),
]
app_name = "settingApi"
