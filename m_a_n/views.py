from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.db.models import Sum
from django.contrib import messages
import bcrypt
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'log_reg.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def go_home_roger(request):
    if 'user_name' not in request.session:
        redirect('/')
    context = {
        'all_shops': Shop.objects.all()
    }
    return render(request, 'master_home.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_val(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            username=request.POST['username'],email=request.POST['email'],password=pw_hash)
        request.session['user_name'] = new_user.username
        request.session['user_id'] = new_user.id
        return redirect('/master_home')
    return redirect('/')    

def user_logger(request):
    if request.method == 'POST':
        errors = User.objects.login_val(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user):
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_name'] = logged_user.username
                request.session['user_id'] = logged_user.id
                return redirect('/master_home')
    return redirect('/')    

def new_shop(request):
    if 'user_name' not in request.session:
        redirect('/')
    return render(request, 'create_shop.html')

def create_shop(request):
    if request.method == 'POST':
        errors = Shop.objects.shop_val(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_shop')
        one_shop = Shop.objects.create(shop_name=request.POST['shop_name'], shop_type=request.POST['shop_type'], creator=User.objects.get(id=request.session['user_id']))
        request.session['shop_id'] = one_shop.id
        return redirect(f'shop/{str(one_shop.id)}')
    return redirect('/')

def one_shop(request, id):
    context = {
        'one_shop': Shop.objects.get(id=id),
        
    }
    return render(request, 'shop.html', context)

def new_product(request):
    if 'user_name' not in request.session:
        redirect('/')
    return render(request, 'create_product.html')

def create_product(request):
    if request.method == 'POST':
        errors = Product.objects.product_val(request.POST)
        print(errors)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new_product')
        new_product = Product.objects.create(product_name=request.POST['product_name'], price=request.POST['product_price'], description=request.POST['description'], shop=Shop.objects.get(id=request.session['shop_id']),product_pic = request.FILES['product_pic'])   
        return redirect(f'product/{str(new_product.id)}')
    return redirect('/')

def one_product(request, id):

    context = {
        'one_product': Product.objects.get(id=id),

    }
    return render(request, 'product.html', context)

def delete(request, id):
        Product.objects.get(id=id).delete()
        return redirect ('/master_home')

def my_shops(request, id):
    context = {
        'one_user': User.objects.get(id=id)
    }
    return render(request, 'my_shops.html', context)

def purchase(request):
    if request.method == 'POST':
        this_product = Product.objects.filter(id=request.POST["id"])
        if not this_product:
            return redirect('/')
        else:
            quantity = int(request.POST["quantity"])
            total_charge = quantity*(float(this_product[0].price))
            Order.objects.create(quantity_ordered=quantity, total_price=total_charge)
            return redirect('/checkout')
    return redirect('/')

def checkout(request):
    last = Order.objects.last()
    price=last.total_price
    full_order = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    full_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    context = {
        'orders':full_order,
        'total':full_price,
        'bill':price,
    }
    return render(request, 'checkout.html' ,context)

