from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from Store.models import Product
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = authenticate(request, username=username, password=password)
        if admin and admin.is_staff:
            login(request, admin)
            return redirect('add_product')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'admin/admin_login.html')

def add_product(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        image = request.FILES.get('image')
        Product.objects.create(name=name, description=description, price=price, image=image)
        messages.success(request, 'Product added successfully.')
        return redirect('add_product')
    return render(request, 'admin/add_product.html')
