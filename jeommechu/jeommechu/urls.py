# jeommechu/urls.py
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.static import serve
from django.urls import re_path



urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('maps/', include('maps.urls')),
    path('accounts/', include('allauth.urls')),  # django-allauth
    path('reviews/', include('reviews.urls')),

]
