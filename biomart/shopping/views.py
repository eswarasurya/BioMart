from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import date
import uuid, requests, json
from .models import Product, Review
from .forms import ProductRegistrationForm, ReviewForm
from accounts.forms import BuyerRegistrationForm
from newsapi import NewsApiClient
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

def articles_view(request):
    # api_key='09561e18b4bc466f9f25d198419d990b'
    news_api_request = requests.get("http://newsapi.org/v2/everything?q=organic+food+india&apiKey=09561e18b4bc466f9f25d198419d990b")
    context = json.loads(news_api_request.content)
    return render(request, 'shopping/blog.html', {'context':context})

def about_view(request):
    mapbox_access_token = 'pk.eyJ1IjoicmFnaHVyYW0xMjMiLCJhIjoiY2tnbnh2ZW83MDc3cjJ6bW5uYWFqeTU0dCJ9.gcokX86DNr2GNnD57ZGEmw'
    return render(request, 'about.html',{ 'mapbox_access_token': mapbox_access_token })

def base_view(request):
    return render(request, 'base.html')

def all_products(request):
    products = Product.objects.all()
    return render(request, 'shopping/all_products.html', {'products':products})

def add_products(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_seller.html', {'form':form})
    is_seller = False
    try:
        if request.user.seller is not None:
            is_seller = True
    except:
        pass
    form = ProductRegistrationForm
    if not is_seller:
        return render(request, 'shopping/add_products.html', {'form':form, 'error':'You are not allowed to add products, try logging in with seller account'})
    if request.method == 'POST':
        form = ProductRegistrationForm(request.POST)
        if form.is_valid():
            new_prod = Product()
            new_prod.product_name = form.cleaned_data['product_name']
            new_prod.mrp = form.cleaned_data['mrp']
            new_prod.discount = form.cleaned_data['discount']
            new_prod.price = form.cleaned_data['price']
            new_prod.description = form.cleaned_data['description']
            new_prod.quantity = form.cleaned_data['quantity']
            new_prod.origin = form.cleaned_data['origin']
            new_prod.sold_by = request.user
            request.user.seller.sell_items.append(new_prod.productid)
            request.user.seller.save()
            new_prod.save()
            return redirect('all_products')
    return render(request, 'shopping/add_products.html', {'form':form})


def is_seller(request):
    try:
        if request.user.seller:
            return True
    except:
        return False


def is_present_in_arr(arr, id):
    for i in range(0, len(arr)):
        temp = arr[i].split(' ')
        if temp[0] == str(id):
            return i
    return -1


def add_to_cart(request, productid):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})

    if is_seller(request):
        test_index = is_present_in_arr(request.user.seller.sell_items, productid)
        print(test_index)
        if test_index != -1:    # Seller cannot buy his own items
            return redirect('all_products')
        index = is_present_in_arr(request.user.seller.cart_items, productid)
        if index == -1:
            request.user.seller.cart_items.append(str(productid) + ' ' + '1')
        else:
            temp = request.user.seller.cart_items[index].split(' ')
            temp[1] = int(temp[1]) + 1  #incrementing count
            request.user.seller.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        request.user.seller.save()

    else:
        index = is_present_in_arr(request.user.buyer.cart_items, productid)
        if index == -1:
            request.user.buyer.cart_items.append(str(productid) + ' ' + '1')
        else:
            temp = request.user.buyer.cart_items[index].split(' ')
            temp[1] = int(temp[1]) + 1  #incrementing count
            request.user.buyer.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        messages.success(request, 'Product added to cart')
        request.user.buyer.save()

    return redirect('all_products')


def cart(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})
    usr = User.objects.get(username=request.user.username)
    is_seller = False
    try:
        if request.user.seller:
            is_seller = True
    except:
        pass
    if not is_seller:
        items = request.user.buyer.cart_items
    else:
        items = request.user.seller.cart_items
    data = []
    total = 0
    count = 0
    for x in items:
        temp = x.split(" ")
        prod = Product.objects.get(pk=temp[0])
        # prod.quantity = prod.quantity * float(temp[1])
        # prod.price = prod.price * float(temp[1])
        total += float(temp[1]) * prod.price
        count += 1
        data.append([prod, temp[1]])
    return render(request, 'shopping/cart.html', {'data':data, 'total':total, 'count':count, })


def increament_count_cart(request, productid):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})
    if is_seller(request):
        items = request.user.seller.cart_items
        index = is_present_in_arr(request.user.seller.cart_items, productid)
        if index == -1: # product doesn't exist in cart
            pass
        else:
            temp = request.user.seller.cart_items[index].split(' ')
            if int(temp[1]) >= 1:
                temp[1] = int(temp[1]) + 1
                request.user.seller.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        request.user.seller.save()
    else:
        items = request.user.buyer.cart_items
        index = is_present_in_arr(request.user.buyer.cart_items, productid)
        if index == -1: # product doesn't exist in cart
            pass
        else:
            temp = request.user.buyer.cart_items[index].split(' ')
            if int(temp[1]) >= 1:
                temp[1] = int(temp[1]) + 1
                request.user.buyer.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        request.user.buyer.save()


    total = 0
    for x in items:
        temp = x.split(" ")
        prod = Product.objects.get(pk=temp[0])
        total += float(temp[1]) * prod.price
    resp_data = {
            'html': total,
        }
    print(total)
    return JsonResponse(resp_data, status=200)



def decreament_count_cart(request, productid):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})
    if is_seller(request):
        items = request.user.seller.cart_items
        index = is_present_in_arr(request.user.seller.cart_items, productid)
        if index == -1: # product doesn't exist in cart
            pass
        else:
            temp = request.user.seller.cart_items[index].split(' ')
            if int(temp[1]) > 1:
                temp[1] = int(temp[1]) - 1
                request.user.seller.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        request.user.seller.save()
    else:
        items = request.user.buyer.cart_items
        index = is_present_in_arr(request.user.buyer.cart_items, productid)
        if index == -1: # product doesn't exist in cart
            pass
        else:
            temp = request.user.buyer.cart_items[index].split(' ')
            if int(temp[1]) > 1:
                temp[1] = int(temp[1]) - 1
                request.user.buyer.cart_items[index] = str(temp[0]) + ' ' + str(temp[1])
        request.user.buyer.save()
    
    total = 0
    for x in items:
        temp = x.split(" ")
        prod = Product.objects.get(pk=temp[0])
        total += float(temp[1]) * prod.price
    resp_data = {
            'html': total,
        }
    print(total)
    return JsonResponse(resp_data, status=200)




def remove_from_cart(request, productid):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})

    if is_seller(request):
        index = is_present_in_arr(request.user.seller.cart_items, productid)
        if index == -1:
            pass
        else:
            temp = request.user.seller.cart_items[index].split(' ')
            temp1 = request.user.seller.cart_items[index]
            request.user.seller.cart_items.remove(temp1)
        request.user.seller.save()
    else:
        index = is_present_in_arr(request.user.buyer.cart_items, productid)
        if index == -1:
            pass
        else:
            temp = request.user.buyer.cart_items[index].split(' ')
            temp1 = request.user.buyer.cart_items[index]
            request.user.buyer.cart_items.remove(temp1)
        request.user.buyer.save()
    
    return redirect('cart')



def checkout(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})
    if is_seller(request):
        for x in request.user.seller.cart_items:
            request.user.seller.brought_items.append(x + ' ' + str(date.today()))
        
        for x in request.user.seller.cart_items:
            temp = x.split(' ')
            sold_by = Product.objects.get(pk=temp[0]).sold_by   
            sold_by.seller.sold_items.append(x + ' ' + str(date.today()))
            # sold_by.save()
            sold_by.seller.save() 
        request.user.seller.cart_items = []
        request.user.seller.save()
    else:
        for x in request.user.buyer.cart_items:
            request.user.buyer.brought_items.append(x + ' ' + str(date.today()))
            temp = x.split(' ')
            sold_prod = Product.objects.get(pk=temp[0])
            sold_prod.sold_by.seller.sold_items.append(x + ' ' + str(date.today()))
            sold_prod.sold_by.seller.save() 
        request.user.buyer.cart_items = []
        request.user.buyer.save()
    return redirect('all_products')

def reviews(request):
    data = Review.objects.all()
    context = {'data':data}
    return render(request,'shopping/all_reviews.html',context)

def add_review(request):
    if not request.user.is_authenticated:
        form = BuyerRegistrationForm()
        return render(request, 'accounts/register_buyer.html', {'form':form})
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_rev = Review()
            new_rev.product = form.cleaned_data['product']
            new_rev.reviewby = request.user
            new_rev.stars = form.cleaned_data['stars']
            new_rev.review = form.cleaned_data['review']
            new_rev.save()
            return redirect('reviews')
    return render(request, 'shopping/add_review.html', {'form':form})
