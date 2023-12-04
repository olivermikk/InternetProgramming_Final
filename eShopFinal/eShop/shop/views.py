from django.shortcuts import render
from .forms import ImageForm


# Create your views here.

def shop(request):
    return render((request, 'index.html', {}))




def products(request):
    if request.method == 'GET':
 
        # getting all the objects of hotel.
        product = shop.objects.all()
        return render((request, 'index.html', {'images': product}))

