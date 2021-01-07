from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.utils import timezone
from .models import loc
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView

# Create your views here.
def alllocs(request):
	if not request.user.is_authenticated:
		return render(request, 'accounts/login.html')
	all_locs_temp = loc.objects.all()
	return render(request, 'locations/alllocs.html', {'all_locs':all_locs_temp})

def add(request):
	if not request.user.is_authenticated:
		return render(request, 'accounts/login.html')
	if request.method == 'POST':
		if request.POST['bno'] and request.POST['street'] and request.POST['area'] and request.POST['state']:
			new_loc = loc()
			new_loc.bno = request.POST['bno']
			new_loc.street = request.POST['street']
			new_loc.area = request.POST['area']
			new_loc.state = request.POST['state']
			new_loc.owner = request.user
			new_loc.save()
			return redirect('alllocs')
		else:
			return render(request, 'locations/add_loc.html', {'error':'all fields required'})
	else:
		return render(request, 'locations/add_loc.html')


def mylocs(request):
	loc_list = []
	data = loc.objects.all()
	for z in data:
		# curr_blog = blog.objects.get(pk = z['pk'])
		if z.owner == request.user:
			loc_list.append(z)
	return render(request, 'locations/mylocs.html', {'loc_list':loc_list})


def delete_loc(request, loc_id):
	if not request.user.is_authenticated:
		return render(request, 'accounts/login.html')
	curr_loc = loc.objects.get(pk = loc_id)
	curr_loc.delete()
	return redirect('alllocs')

