from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.alllocs, name = 'alllocs'),
    path('add/', views.add, name='add'),
    path('mylocs/',views.mylocs, name = 'mylocs'),
    path('<int:loc_id>/delete_loc/', views.delete_loc, name = 'delete_loc'),
    path('api/', include('locations.api.urls')),
    # path('', HomePageView.as_view(), name='allblogs'),
]