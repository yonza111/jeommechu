# maps/serializers.py
from rest_framework import serializers

class RestaurantSerializer(serializers.Serializer):
    place_name = serializers.CharField()  # 장소 이름
    road_address_name = serializers.CharField()  # 도로명 주소
    address_name = serializers.CharField()  # 지번 주소
    category_name = serializers.CharField()  # 카테고리
    place_url = serializers.URLField()  # 카카오 장소 URL
    menu = serializers.CharField(default="Sample Menu")  # 메뉴 데이터는 API 확장을 통해 추가 가능
    opening_hours = serializers.CharField(default="9:00 AM - 10:00 PM")  # 영업시간도 필요 시 API 확장

class CafeSerializer(serializers.Serializer):
    place_name = serializers.CharField()  # 장소 이름
    road_address_name = serializers.CharField()  # 도로명 주소
    address_name = serializers.CharField()  # 지번 주소
    place_url = serializers.URLField()  # 카카오 장소 URL
    menu = serializers.CharField(default="Sample Menu")  # 메뉴 데이터는 API 확장을 통해 추가 가능
    opening_hours = serializers.CharField(default="9:00 AM - 10:00 PM")  # 영업시간도 필요 시 API 확장