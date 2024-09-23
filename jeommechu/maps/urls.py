from django.urls import path
from .views import RestaurantListView, CafeListView

urlpatterns = [
    path('restaurants_nearby/', RestaurantListView.as_view(), name='restaurants_nearby'),
    path('cafes_nearby/', CafeListView.as_view(), name='cafes_nearby'),
]
