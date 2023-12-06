from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, User



# Create your views here.

def shop(request):
    return render(request, 'shop/index.html', {})


def products(request):

    qs = Product.objects.all()
    context = {
        'objects' : qs
    }

        
    return render(request, "shop/products.html", context)

def productDetails(request, name):
    qs = get_object_or_404(Product, name=name)
    context = {
        'object': qs
    }
    return render(request, "shop/productDetails.html", context)




def category(request):
    return(request, "shop/products.html")




def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'shop/cart.html', {'user': request.user, 'cart': cart})
    else:
        return render(request, 'shop/cart.html', {'user': None, 'cart': None})
    

def add_to_cart(request, name):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, name=name)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return redirect('shop:cart')
    else:
        return redirect('login')  # Redirect to login page if the user is not authenticated


def remove_from_cart(request, name):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, name=name)
        cart = get_object_or_404(Cart, user=request.user)
        cart.products.remove(product)
        return redirect('shop:cart')
    else:
        return redirect('login')  # Redirect to login page if the user is not authenticated




