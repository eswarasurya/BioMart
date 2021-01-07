from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.allblogs, name = 'allblogs'),
    path('create/', views.create, name='create'),
    path('myblogs/',views.myblogs, name = 'myblogs'),
    path('<int:blog_id>/delete_blog/', views.delete_blog, name = 'delete_blog'),
    path('api/', include('blogs.api.urls')),
    # path('', HomePageView.as_view(), name='allblogs'),
]