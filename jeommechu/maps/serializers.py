from rest_framework import serializers

class RestaurantSerializer(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()
    category = serializers.CharField()
    # distance = serializers.IntegerField() 어차피 반경 1km라고 정하므로 distance 빼기로 함. 지도에서 확인도 되고
    link = serializers.URLField()
    menu = serializers.CharField()
    opening_hours = serializers.CharField()

class CafeSerializer(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()
    # distance = serializers.IntegerField() 어차피 반경 1km라고 정하므로 distance 빼기로 함. 지도에서 확인도 되고
    link = serializers.URLField()
