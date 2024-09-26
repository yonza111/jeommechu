from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import urllib.parse
import os
import urllib.request
from django.shortcuts import render
from .serializers import RestaurantSerializer, CafeSerializer
import json
from dotenv import load_dotenv
import re

load_dotenv()

def search_nearby_places(lat, lon, query, radius):
    kakao_api_key = os.environ.get('KAKAO_API_KEY')  # 카카오 REST API 키

    # 카카오 API URL 구성 (x는 경도, y는 위도)
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={urllib.parse.quote(query)}&x={lon}&y={lat}&radius={radius}&size=15"  # 최대 15개 표시

    request = urllib.request.Request(url)
    request.add_header("Authorization", f"KakaoAK {kakao_api_key}")

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result_json = json.loads(response_body.decode('utf-8'))
        return result_json['documents']  # 결과 리스트 반환
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
                'place_name': item['place_name'],  # 장소 이름
                'road_address_name': item['road_address_name'],  # 도로명 주소
                'address_name': item['address_name'],  # 지번 주소
                'category_name': item.get('category_name', '음식점'),  # 카테고리
                'place_url': item['place_url'],  # 카카오 장소 URL
                'menu': "Sample Menu",  # 메뉴 데이터는 직접 추가 가능
                'opening_hours': "9:00 AM - 10:00 PM",  # 영업시간 역시 직접 추가 가능
            }
            categorized_restaurants.append(restaurant_data)

        serializer = RestaurantSerializer(categorized_restaurants, many=True)
        return Response(serializer.data)

def restaurant_nearby_view(request):
    return render(request, 'restaurant_nearby_kakao.html')   # test template 넣어뒀음(임시)


def get_coordinates_from_address(road_address):
    kakao_api_key = os.environ.get('KAKAO_API_KEY')
    url = f"https://dapi.kakao.com/v2/local/search/address.json?query={urllib.parse.quote(road_address)}"

    request = urllib.request.Request(url)
    request.add_header("Authorization", f"KakaoAK {kakao_api_key}")

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        result_json = json.loads(response_body.decode('utf-8'))
        
        if result_json['documents']:
            # 좌표 정보 추출
            location_data = result_json['documents'][0]['address']
            return {
                'x': location_data['x'],  # 경도
                'y': location_data['y']   # 위도
            }
        else:
            return None
    else:
        return None


def search_nearby_cafes_by_address(road_address):
    # 1. 도로명 주소로 좌표를 먼저 얻음
    coordinates = get_coordinates_from_address(road_address)

    if not coordinates:
        return {"error": "Failed to retrieve coordinates"}

    # 2. 좌표를 기반으로 카페 검색 (반경 100m)
    latitude = coordinates['y']
    longitude = coordinates['x']

    return search_nearby_places(latitude, longitude, "카페", 100)


class CafeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        road_address = request.query_params.get('road_address')

        # 도로명 주소가 없으면 오류를 반환
        if not road_address:
            return Response({"error": "Missing road_address"}, status=400)

        try:
            # 도로명 주소를 이용하여 반경 100m 내 카페 검색
            cafes = search_nearby_cafes_by_address(road_address)

            # 시리얼라이저로 데이터 반환
            serializer = CafeSerializer(cafes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)



def cafe_nearby_view(request):
    return render(request, 'cafes_nearby_kakao.html') # test template 넣어뒀음(임시)