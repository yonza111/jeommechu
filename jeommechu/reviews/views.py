# reviews/views.py
from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from maps.models import Restaurant, Cafe, UserSelection
from .models import RestaurantReview, CafeReview, RestaurantCafeRating
from .serializers import RestaurantReviewSerializer, CafeReviewSerializer, RestaurantCafeRatingSerializer
from .forms import RestaurantReviewForm, CafeReviewForm, RestaurantCafeRatingForm
from maps.serializers import RestaurantSerializer, CafeSerializer
from maps.views import search_nearby_places

class ReviewMainPageView(APIView):
    def get(self, request):
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return redirect('/accounts/login/?next=/reviews/main/')

        # 로그인한 유저가 선택한 UserSelection 가져오기
        user_selections = UserSelection.objects.filter(user=request.user)
        selections_with_review_info = []

        for selection in user_selections:
            # 셋 다 존재해야 True
            review_exists = (
                RestaurantReview.objects.filter(user=request.user, restaurant=selection.restaurant).exists() and
                CafeReview.objects.filter(user=request.user, cafe=selection.cafe).exists() and
                RestaurantCafeRating.objects.filter(user=request.user, restaurant=selection.restaurant, cafe=selection.cafe).exists()
            )

            selections_with_review_info.append({
                'selection': selection,
                'review_exists': review_exists,  # 리뷰 존재 여부
            })

        return render(request, 'reviews/main.html', {'selections': selections_with_review_info})
    
class NearbyReviewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if not latitude or not longitude:
            return Response({"error": "위도와 경도를 제공해야 합니다."}, status=400)

        # 1km 반경 내 음식점 검색
        restaurants = search_nearby_places(latitude, longitude, "음식점", 1000)

        restaurant_reviews_with_data = []
        cafe_reviews_with_data = []
        restaurant_cafe_reviews_with_data = []

        for restaurant in restaurants:
            restaurant_obj = Restaurant.objects.filter(place_name=restaurant['place_name']).first()
            if restaurant_obj:
                # 음식점 리뷰
                restaurant_reviews = RestaurantReview.objects.filter(restaurant=restaurant_obj)
                if restaurant_reviews.exists():
                    serialized_reviews = RestaurantReviewSerializer(restaurant_reviews, many=True).data
                    restaurant['reviews'] = serialized_reviews
                    restaurant_reviews_with_data.append(restaurant)

                # 해당 음식점과 연결된 카페-쌍 가져오기
                user_selections = UserSelection.objects.filter(restaurant=restaurant_obj)
                
                for selection in user_selections:
                    cafe = selection.cafe
                    # 카페 리뷰
                    cafe_reviews = CafeReview.objects.filter(cafe=cafe)
                    if cafe_reviews.exists():
                        serialized_reviews = CafeReviewSerializer(cafe_reviews, many=True).data
                        cafe_data = {
                            "place_name": cafe.place_name,
                            "reviews": serialized_reviews
                        }
                        cafe_reviews_with_data.append(cafe_data)
                    
                    # 음식점-카페 쌍에 대한 리뷰
                    restaurant_cafe_reviews = RestaurantCafeRating.objects.filter(restaurant=restaurant_obj, cafe=cafe)
                    if restaurant_cafe_reviews.exists():
                        serialized_reviews = RestaurantCafeRatingSerializer(restaurant_cafe_reviews, many=True).data
                        restaurant_cafe_reviews_with_data.append({
                            "restaurant": restaurant['place_name'],
                            "cafe": cafe.place_name,
                            "reviews": serialized_reviews
                        })

        # 음식점, 카페 및 음식점-카페 쌍에 대한 리뷰 데이터를 직렬화하여 반환
        return Response({
            "restaurants_with_reviews": restaurant_reviews_with_data,
            "cafes_with_reviews": cafe_reviews_with_data,
            "restaurant_cafe_reviews": restaurant_cafe_reviews_with_data
        })



class ReviewsNearbyTemplateView(TemplateView):
    template_name = 'reviews/reviews_nearby.html'




class AllReviewCreateView(View):
    def get(self, request, restaurant_id, cafe_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        cafe = Cafe.objects.get(id=cafe_id)

        # 각 폼에 prefix 추가
        restaurant_form = RestaurantReviewForm(prefix='restaurant')
        cafe_form = CafeReviewForm(prefix='cafe')
        restaurant_cafe_form = RestaurantCafeRatingForm(prefix='restaurant_cafe')

        return render(request, 'reviews/all_reviews_form.html', {
            'restaurant': restaurant,
            'cafe': cafe,
            'restaurant_form': restaurant_form,
            'cafe_form': cafe_form,
            'restaurant_cafe_form': restaurant_cafe_form
        })

    def post(self, request, restaurant_id, cafe_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        cafe = Cafe.objects.get(id=cafe_id)

        # 각 폼에 prefix 추가하여 POST 데이터 처리
        restaurant_form = RestaurantReviewForm(request.POST, prefix='restaurant')
        cafe_form = CafeReviewForm(request.POST, prefix='cafe')
        restaurant_cafe_form = RestaurantCafeRatingForm(request.POST, prefix='restaurant_cafe')

        if all([restaurant_form.is_valid(), cafe_form.is_valid(), restaurant_cafe_form.is_valid()]):
            # 음식점 리뷰 저장
            restaurant_review = restaurant_form.save(commit=False)
            restaurant_review.user = request.user
            restaurant_review.restaurant = restaurant
            restaurant_review.save()

            # 카페 리뷰 저장
            cafe_review = cafe_form.save(commit=False)
            cafe_review.user = request.user
            cafe_review.cafe = cafe
            cafe_review.save()

            # 음식점+카페 평가 저장
            restaurant_cafe_rating = restaurant_cafe_form.save(commit=False)
            restaurant_cafe_rating.user = request.user
            restaurant_cafe_rating.restaurant = restaurant
            restaurant_cafe_rating.cafe = cafe
            restaurant_cafe_rating.save()

            # 리뷰 작성 완료 후 메인 페이지로 리다이렉트
            return redirect(reverse('review_main_page'))

        return render(request, 'reviews/all_reviews_form.html', {
            'restaurant': restaurant,
            'cafe': cafe,
            'restaurant_form': restaurant_form,
            'cafe_form': cafe_form,
            'restaurant_cafe_form': restaurant_cafe_form
        })

    
class AllReviewDetailView(View):
    def get(self, request, restaurant_id, cafe_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        cafe = Cafe.objects.get(id=cafe_id)

        restaurant_review = RestaurantReview.objects.filter(user=request.user, restaurant=restaurant).first()
        cafe_review = CafeReview.objects.filter(user=request.user, cafe=cafe).first()
        restaurant_cafe_rating = RestaurantCafeRating.objects.filter(user=request.user, restaurant=restaurant, cafe=cafe).first()

        return render(request, 'reviews/all_reviews_detail.html', {
            'restaurant': restaurant,
            'cafe': cafe,
            'restaurant_review': restaurant_review,
            'cafe_review': cafe_review,
            'restaurant_cafe_rating': restaurant_cafe_rating
        })

class AllReviewUpdateView(View):
    def get(self, request, restaurant_id, cafe_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        cafe = Cafe.objects.get(id=cafe_id)

        # 기존 리뷰 불러오기
        restaurant_review = RestaurantReview.objects.filter(user=request.user, restaurant=restaurant).first()
        cafe_review = CafeReview.objects.filter(user=request.user, cafe=cafe).first()
        restaurant_cafe_rating = RestaurantCafeRating.objects.filter(user=request.user, restaurant=restaurant, cafe=cafe).first()

        # 기존 리뷰 정보를 폼에 미리 채워서 전달
        restaurant_form = RestaurantReviewForm(instance=restaurant_review, prefix='restaurant')
        cafe_form = CafeReviewForm(instance=cafe_review, prefix='cafe')
        restaurant_cafe_form = RestaurantCafeRatingForm(instance=restaurant_cafe_rating, prefix='restaurant_cafe')

        return render(request, 'reviews/all_reviews_update_form.html', {
            'restaurant': restaurant,
            'cafe': cafe,
            'restaurant_form': restaurant_form,
            'cafe_form': cafe_form,
            'restaurant_cafe_form': restaurant_cafe_form
        })

    def post(self, request, restaurant_id, cafe_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        cafe = Cafe.objects.get(id=cafe_id)

        # 기존 리뷰 불러오기
        restaurant_review = RestaurantReview.objects.filter(user=request.user, restaurant=restaurant).first()
        cafe_review = CafeReview.objects.filter(user=request.user, cafe=cafe).first()
        restaurant_cafe_rating = RestaurantCafeRating.objects.filter(user=request.user, restaurant=restaurant, cafe=cafe).first()

        # 폼에서 입력된 데이터로 수정
        restaurant_form = RestaurantReviewForm(request.POST, instance=restaurant_review, prefix='restaurant')
        cafe_form = CafeReviewForm(request.POST, instance=cafe_review, prefix='cafe')
        restaurant_cafe_form = RestaurantCafeRatingForm(request.POST, instance=restaurant_cafe_rating, prefix='restaurant_cafe')

        if all([restaurant_form.is_valid(), cafe_form.is_valid(), restaurant_cafe_form.is_valid()]):
            # 리뷰 업데이트 저장
            restaurant_form.save()
            cafe_form.save()
            restaurant_cafe_form.save()

            return redirect(reverse('review_detail', args=[restaurant_id, cafe_id]))

        return render(request, 'reviews/all_reviews_update_form.html', {
            'restaurant': restaurant,
            'cafe': cafe,
            'restaurant_form': restaurant_form,
            'cafe_form': cafe_form,
            'restaurant_cafe_form': restaurant_cafe_form
        })


