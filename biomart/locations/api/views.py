from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from locations.models import loc
from .serializers import LocationSerializer, LocationSerializerPost
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone


@api_view(http_method_names=['GET', 'POST', ])
@permission_classes([IsAuthenticated])
def loc_list_view(request):
    if request.method == 'GET':
        return loc_list_view_get(request)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error':'You are not authenticated'}) 
    return loc_list_view_post(request)

def loc_list_view_get(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 5
        data = loc.objects.all()
        result_page = paginator.paginate_queryset(data, request)
        serializer = LocationSerializer(result_page,many=True)
        return paginator.get_paginated_response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def loc_list_view_post(request):
    hdata = loc(owner = request.user)
    serializer = LocationSerializerPost(hdata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

