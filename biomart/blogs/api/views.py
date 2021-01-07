from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from blogs.models import blog
from .serializers import BlogSerializer, BlogSerializerPost
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone


@api_view(http_method_names=['GET', 'POST', ])
@permission_classes([IsAuthenticated])
def Blog_list_view(request):
    if request.method == 'GET':
        return blog_list_view_get(request)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error':'You are not authenticated'}) 
    return blog_list_view_post(request)

def blog_list_view_get(request):
    try:
        paginator = PageNumberPagination()
        paginator.page_size = 5
        data = blog.objects.all()
        result_page = paginator.paginate_queryset(data, request)
        serializer = BlogSerializer(result_page,many=True)
        return paginator.get_paginated_response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

def blog_list_view_post(request):
    temp = timezone.datetime.now()
    hdata = blog(writer=request.user, pub_date=temp)
    serializer = BlogSerializerPost(hdata, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

