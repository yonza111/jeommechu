
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('maps/', include('maps.urls')),
    path('accounts/', include('allauth.urls')),  # django-allauth
    path('reviews/', include('reviews.urls')),
]
