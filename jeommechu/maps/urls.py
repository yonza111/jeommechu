from django.urls import path
from .views import RestaurantListView, CafeListView, restaurant_template_view_function

urlpatterns = [
    path('api/restaurants_nearby/', RestaurantListView.as_view(), name='restaurants_nearby'),
    path('api/cafes_nearby/', CafeListView.as_view(), name='cafes_nearby'),
    path('restaurants_nearby/', restaurant_template_view_function, name='restaurant_template'),  # HTML 템플릿 렌더링 URL
]