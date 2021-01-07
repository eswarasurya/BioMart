from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('register_buyer/', views.register_buyer, name='register_buyer'),
    path('register_seller/', views.register_seller, name='register_seller'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('buyer_profile/', views.buyer_profile, name='buyer_profile'),
    path('get_token/', views.get_token, name='get_token'),
]
