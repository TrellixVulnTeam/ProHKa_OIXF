from django.contrib import admin
from administration.models import *

# Register your models here.
admin.site.register(UserRegistration)
admin.site.register(Slides)
admin.site.register(ReceiveCommand)
admin.site.register(GlobalSetting)
admin.site.register(Message)