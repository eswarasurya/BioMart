from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('reviews/', views.reviews, name='reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('about/', views.about_view, name='about_view'),
    path('articles/', views.articles_view, name='articles_view'),
    path('base/',views.base_view,name='base_view'),
    path('all_products/', views.all_products, name='all_products'),
    path('add_products/', views.add_products, name='add_products'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<uuid:productid>', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<uuid:productid>', views.remove_from_cart, name = 'remove_from_cart'),
    path('decreament_count_cart/<uuid:productid>', views.decreament_count_cart, name = 'decreament_count_cart'),
    path('increament_count_cart/<uuid:productid>', views.increament_count_cart, name = 'increament_count_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('api/', include('shopping.api.urls')),
]   
