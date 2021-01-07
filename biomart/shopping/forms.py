from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Product, Review

class ProductRegistrationForm(forms.Form):
    product_name = forms.CharField(max_length=100)
    mrp = forms.FloatField()
    discount = forms.FloatField()
    price = forms.FloatField()
    quantity = forms.FloatField(required=False)
    origin = forms.CharField(max_length=200, required=False)
    description = forms.CharField(widget=forms.Textarea)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'stars', 'review']
