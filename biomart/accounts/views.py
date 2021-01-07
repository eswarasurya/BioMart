from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm

from .forms import BuyerRegistrationForm
from .models import Buyer, Seller
from shopping.models import Product
from rest_framework.authtoken.models import Token



# Create your views here.
def register_buyer(request):
    form = BuyerRegistrationForm()
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], password = form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            user_obj = Buyer(user=user, phone=form.cleaned_data['phone'], cart_items=[], brought_items=[])
            user_obj.save()
            auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    return render(request, 'accounts/register_buyer.html', {'form':form})


def register_seller(request):
    form = BuyerRegistrationForm()
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], password = form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            user_obj = Seller(user=user, phone=form.cleaned_data['phone'], sell_items=[], cart_items=[], sold_items=[], brought_items=[])
            user_obj.save()
            auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    return render(request, 'accounts/register_seller.html', {'form':form})


def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
    return render(request,'accounts/login.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def logout(request):
	auth.logout(request)
	return redirect('home')


def is_seller(request):
    try:
        if request.user.seller:
            return True
    except:
        return False



def seller_profile(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/login.html', {'form':form})
    # user_obj = User.objects.get(username=request.user.username)
    sell_items = []
    brought_items = []
    sold_items = []
    if is_seller(request):
        print('sold items: ', request.user.seller.sold_items)
        for x in request.user.seller.sell_items:
            sell_items.append(Product.objects.get(pk=x))

        for x in request.user.seller.sold_items:
            temp = x.split(' ')
            sold_items.append([Product.objects.get(pk=temp[0]), temp[1], temp[2]])

        for x in request.user.seller.brought_items:
            temp = x.split(' ')
            brought_items.append([Product.objects.get(pk=temp[0]), temp[1], temp[2]])

    return render(request, 'accounts/seller_profile.html', {'user':request.user, 'sell_items':sell_items, 'sold_items':sold_items, 'brought_items':brought_items})


def buyer_profile(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/login.html', {'form':form})
    brought_items = []
    if not is_seller(request):
        for x in request.user.buyer.brought_items:
            temp = x.split(' ')
            brought_items.append([Product.objects.get(pk=temp[0]), temp[1], temp[2]])

    return render(request, 'accounts/buyer_profile.html', {'user':request.user, 'brought_items':brought_items})


def get_token(request):
    if not request.user.is_authenticated:
        token = 'You are not authenticated'
        return render(request, 'accounts/token.html', {'token':token})
    token = Token.objects.filter(user=request.user)
    if len(token) == 0:
        token = Token.objects.create(user=request.user)
    return render(request, 'accounts/token.html', {'token':token})
        
