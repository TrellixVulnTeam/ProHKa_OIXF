from rest_framework import serializers
from administration.models import *
from authentication.models import *


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    owner = UserSerializers()

    class Meta:
        model = UserRegistration
        fields = "__all__"


class SettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slides
        fields = "__all__"


class ReceiveCommandSerializers(serializers.ModelSerializer):
    user = UserRegistrationSerializers()

    class Meta:
        model = ReceiveCommand
        fields = "__all__"


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
