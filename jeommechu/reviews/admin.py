from django.contrib import admin
from .models import RestaurantReview, CafeReview, RestaurantCafeRating

admin.site.register(RestaurantReview)
admin.site.register(CafeReview)
admin.site.register(RestaurantCafeRating)
