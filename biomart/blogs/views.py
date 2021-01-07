from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.utils import timezone
from .models import blog
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView

# Create your views here.
def allblogs(request):
	all_blogs_temp = blog.objects.all()
	return render(request, 'blogs/allblogs.html', {'all_blogs':all_blogs_temp})

def create(request):
	if not request.user.is_authenticated:
		return render(request, 'login.html')
	if request.method == 'POST':
		if request.POST['title'] and request.POST['body']:
			new_blog = blog()
			new_blog.title = request.POST['title']
			new_blog.body = request.POST['body']
			new_blog.writer = request.user
			new_blog.pub_date = timezone.datetime.now()
			new_blog.save()
			return redirect('allblogs')
		else:
			return render(request, 'blogs/create_blog.html', {'error':'all fields required'})
	else:
		return render(request, 'blogs/create_blog.html')


def myblogs(request):
	if not request.user.is_authenticated:
		return render(request, 'accounts/register_buyer.html')
	blog_list = []
	data = blog.objects.all()
	for z in data:
		# curr_blog = blog.objects.get(pk = z['pk'])
		if z.writer == request.user:
			blog_list.append(z)
	return render(request, 'blogs/myblogs.html', {'blog_list':blog_list})


def delete_blog(request, blog_id):
	if not request.user.is_authenticated:
		return render(request, 'accounts/register_buyer.html')
	curr_blog = blog.objects.get(pk = blog_id)
	curr_blog.delete()
	return redirect('allblogs')

