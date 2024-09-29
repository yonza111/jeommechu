from django.contrib import admin
from .models import Restaurant, Cafe, UserSelection

admin.site.register(Restaurant)
admin.site.register(Cafe)
admin.site.register(UserSelection)