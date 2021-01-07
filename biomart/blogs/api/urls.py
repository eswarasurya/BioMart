from django.urls import include, path
from . import views

urlpatterns = [
    path('blogs_data',views.Blog_list_view, name="Blog_list_view"),   
]