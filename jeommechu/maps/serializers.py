from rest_framework import serializers

class RestaurantSerializer(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()
    category = serializers.CharField()
    distance = serializers.IntegerField()
    link = serializers.URLField()
    menu = serializers.CharField()
    opening_hours = serializers.CharField()

class CafeSerializer(serializers.Serializer):
    title = serializers.CharField()
    address = serializers.CharField()
    distance = serializers.IntegerField()
    link = serializers.URLField()
