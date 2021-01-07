from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('productsdata',views.Product_list_view, name="product_list_view"),   
    path('origin_data/<slug:slug>',views.Origin_list_view, name="Origin_list_view"),   
]