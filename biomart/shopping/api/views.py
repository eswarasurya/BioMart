from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from shopping.models import Product
from .serializers import ProductSerializer, OriginSerializer, ProductPostSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import uuid

@api_view(http_method_names=['GET', 'POST', ])
@permission_classes([IsAuthenticated])
def Product_list_view(request):
    if request.method == 'GET':
        return product_list_view_get(request)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error':'You are not authenticated'})
    is_seller = False
    try:
        if request.user.seller is not None:
            is_seller = True
    except:
        pass
    if not is_seller:
        return JsonResponse({'error':'You are not allowed to add products'})    
    return product_list_view_post(request)

def product_list_view_get(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 10
        data = Product.objects.all()
        result_page = paginator.paginate_queryset(data, request)
        serializer = ProductSerializer(result_page,many=True)
        return paginator.get_paginated_response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def product_list_view_post(request):
    temp = uuid.uuid4()
    request.user.seller.sell_items.append(temp)
    request.user.seller.save()
    pdata = Product(productid=temp, sold_by=request.user)
    serializer = ProductPostSerializer(pdata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=['GET',])
@permission_classes([IsAuthenticated])
def Origin_list_view(request, slug):
    if request.method == 'GET':
        return origin_list_view_get(request, slug)

def origin_list_view_get(request, slug):
    try:
        data = Product.objects.all()
        obj = []
        for x in data:
            if x.product_name.lower().find(slug.lower()) != -1:
                obj.append(x)
        serializer = OriginSerializer(obj,many=True)
        return Response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


