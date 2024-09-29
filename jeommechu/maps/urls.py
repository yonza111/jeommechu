from django.urls import path
from .views import RestaurantListView, CafeListView, restaurant_nearby_view, cafe_nearby_view, SaveSelectionView

urlpatterns = [
    path('api/restaurants_nearby/', RestaurantListView.as_view(), name='restaurants_nearby'),
    path('api/cafes_nearby/', CafeListView.as_view(), name='cafes_nearby'),
    path('api/save_selection/', SaveSelectionView.as_view(), name='save_selection'),
    
    path('restaurants_nearby/', restaurant_nearby_view, name='restaurant_template'),  # HTML 템플릿 렌더링 URL
    path('cafes_nearby/', cafe_nearby_view, name='cafe_nearby'),  # 템플릿 렌더링 URL
    
]