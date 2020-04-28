from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Type)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(State)
admin.site.register(TeleCallDoctors)
admin.site.register(Links)
