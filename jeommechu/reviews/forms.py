from django import forms
from .models import RestaurantReview, CafeReview, RestaurantCafeRating

class RestaurantReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect(attrs={'name': 'restaurant_rating'})) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'name': 'restaurant_comment'}), required=False)

    class Meta:
        model = RestaurantReview
        fields = ['rating', 'comment']


class CafeReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect(attrs={'name': 'cafe_rating'}))  
    comment = forms.CharField(widget=forms.Textarea(attrs={'name': 'cafe_comment'}), required=False)

    class Meta:
        model = CafeReview
        fields = ['rating', 'comment']


class RestaurantCafeRatingForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect(attrs={'name': 'restaurant_cafe_rating'}))  
    comment = forms.CharField(widget=forms.Textarea(attrs={'name': 'restaurant_cafe_comment'}), required=False)

    class Meta:
        model = RestaurantCafeRating
        fields = ['rating', 'comment']
