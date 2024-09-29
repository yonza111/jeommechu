from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    place_name = models.CharField(max_length=255)  # 음식점 이름
    place_url = models.URLField()  # 카카오 지도 URL
    road_address_name = models.CharField(max_length=255)  # 도로명 주소

    def __str__(self):
        return f'{self.place_name} {self.road_address_name} {self.place_url}'

class Cafe(models.Model):
    place_name = models.CharField(max_length=255)  # 카페 이름
    place_url = models.URLField()  # 카카오 지도 URL
    road_address_name = models.CharField(max_length=255)  # 도로명 주소

    def __str__(self):
        return f'{self.place_name} {self.road_address_name} {self.place_url}'

class UserSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 카카오 로그인한 유저와 연결
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # 음식점과 연결
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)  # 카페와 연결
    created_at = models.DateTimeField(auto_now_add=True)  # 선택 시간

    def __str__(self):
        return f"{self.user.id} selected {self.restaurant.place_name} and {self.cafe.place_name}"


