from django.contrib import admin
from botapp.models import *

admin.site.register(Task)
admin.site.register(Action)
admin.site.register(Group)
admin.site.register(TelegramToken)
admin.site.register(ViberToken)

# Register your models here.
