from rest_framework import serializers
from administration.models import *
from authentication.models import *


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"