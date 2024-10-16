# reviews/urls.py
from django.urls import path
from .views import (
    ReviewMainPageView,
    AllReviewCreateView,
    AllReviewDetailView,
    AllReviewUpdateView,
    NearbyReviewsView,
    ReviewsNearbyTemplateView
)

urlpatterns = [
    path('main/', ReviewMainPageView.as_view(), name='review_main_page'),
    path('reviews_nearby/', ReviewsNearbyTemplateView.as_view(), name='reviews_nearby'),
    path('api/reviews_nearby/', NearbyReviewsView.as_view(), name='reviews_nearby_api'),
    path('all_reviews/create/<int:restaurant_id>/<int:cafe_id>/', AllReviewCreateView.as_view(), name='create_all_reviews'),
    path('all_reviews/detail/<int:restaurant_id>/<int:cafe_id>/', AllReviewDetailView.as_view(), name='review_detail'),
    path('all_reviews/update/<int:restaurant_id>/<int:cafe_id>/', AllReviewUpdateView.as_view(), name='update_all_reviews'),

    
    ]