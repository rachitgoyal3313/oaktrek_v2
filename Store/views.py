from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_ids)
    return render(request, 'store/cart.html', {'products': products})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    request.session['cart'] = []
    return render(request, 'store/checkout.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Message sent successfully.')
        return redirect('contact')
    return render(request, 'store/contact.html')
