# reviews/serializers.py
from rest_framework import serializers
from .models import RestaurantReview, CafeReview, RestaurantCafeRating
from maps.models import UserSelection

class UserSelectionSerializer(serializers.ModelSerializer):
    restaurant_place_name = serializers.CharField(source='restaurant.place_name')
    cafe_place_name = serializers.CharField(source='cafe.place_name')

    class Meta:
        model = UserSelection
        fields = ['restaurant_place_name', 'cafe_place_name', 'created_at']

class RestaurantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantReview
        fields = ['id', 'user', 'restaurant', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class CafeReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeReview
        fields = ['id', 'user', 'cafe', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class RestaurantCafeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCafeRating
        fields = ['id', 'user', 'restaurant', 'cafe', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']
