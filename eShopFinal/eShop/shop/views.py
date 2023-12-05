from django.shortcuts import render
from .models import Product


# Create your views here.

def shop(request):
    return render(request, 'shop/index.html', {})




def products(request):
    qs = Product.objects.all()
    context = {
        'objects' : qs
    }
    return render(request, "shop/products.html", context)

