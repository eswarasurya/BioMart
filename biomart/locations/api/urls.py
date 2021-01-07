from django.urls import include, path
from . import views

urlpatterns = [
    path('locs_data',views.loc_list_view, name="loc_list_view"),   
]