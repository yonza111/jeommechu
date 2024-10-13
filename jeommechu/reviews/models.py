# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from maps.models import Restaurant, Cafe  # 기존에 있는 Restaurant, Cafe 모델 임포트

# 음식점 리뷰 모델
class RestaurantReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 리뷰 작성자
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # 리뷰 대상 음식점
    rating = models.IntegerField()  # 별점 (1~5)
    comment = models.TextField()  # 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    def __str__(self):
        return f'{self.restaurant.place_name} - {self.rating} stars by {self.user.username}'

# 카페 리뷰 모델
class CafeReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 리뷰 작성자
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)  # 리뷰 대상 카페
    rating = models.IntegerField()  # 별점 (1~5)
    comment = models.TextField()  # 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    def __str__(self):
        return f'{self.cafe.place_name} - {self.rating} stars by {self.user.username}'

# 음식점-카페 쌍에 대한 평가 모델
class RestaurantCafeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 평점 작성자
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # 음식점
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)  # 카페
    rating = models.IntegerField()  # 별점 (1~5)
    comment = models.CharField(max_length=255, blank=True)  # 간단한 코멘트
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    def __str__(self):
        return f'{self.user.username} rated {self.restaurant.place_name} and {self.cafe.place_name} - {self.rating} stars'
