from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import urllib.request
import json
from .serializers import RestaurantSerializer, CafeSerializer

def search_nearby_places(lat, lon, query, radius):
    client_id = "YOUR_NAVER_CLIENT_ID"
    client_secret = "YOUR_NAVER_CLIENT_SECRET"
    display = 20  # 한 번에 표시할 검색 결과 수

    url = f"https://openapi.naver.com/v1/search/local.json?query={query}&display={display}&sort=random&radius={radius}&start=1&coordinate={lon},{lat}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result_json = json.loads(response_body.decode('utf-8'))
        return result_json['items']
    else:
        return []

class RestaurantListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # 1km 반경 내의 음식점 검색
        restaurants = search_nearby_places(latitude, longitude, "음식점", 1000)

        categorized_restaurants = []
        for item in restaurants:
            restaurant_data = {
                'title': item['title'],
                'address': item['address'],
                'category': item.get('category', '음식점'),
                'distance': item['distance'],
                'link': item['link'],
                'menu': "Sample Menu",  # 메뉴 데이터는 API 확장을 통해 추가 가능
                'opening_hours': "9:00 AM - 10:00 PM",  # 영업시간 역시 API 확장을 통해 추가
            }
            categorized_restaurants.append(restaurant_data)

        serializer = RestaurantSerializer(categorized_restaurants, many=True)
        return Response(serializer.data)

class CafeListView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        restaurant_lat = request.data.get('latitude')
        restaurant_lon = request.data.get('longitude')

        # 100m 반경 내 카페 검색
        cafes = search_nearby_places(restaurant_lat, restaurant_lon, "카페", 100)

        cafe_list = []
        for item in cafes:
            cafe_data = {
                'title': item['title'],
                'address': item['address'],
                'distance': item['distance'],
                'link': item['link'],
            }
            cafe_list.append(cafe_data)

        serializer = CafeSerializer(cafe_list, many=True)
        return Response(serializer.data)
