from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Category, UserInteraction, Rating
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required

class HomeView(ListView):
    model = Category
    template_name = 'eShop/templates/layout.html'
    
def products(request):
    categories = Category.objects.all()
    qs = Product.objects.all()
    context = {
        'objects' : qs,
        'categories': categories,
    }
    return render(request, "shop/products.html", context)

def productDetails(request, name):
    product = get_object_or_404(Product, name=name)
    context = {
        'object': product
    }

    # Create a UserInteraction instance for the 'view' action
    if request.user.is_authenticated:
        UserInteraction.objects.create(user=request.user, action_type='view', product=product)

    return render(request, "shop/productDetails.html", context)

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        user = request.user
        recommended_products = get_recommendations(user)
        return render(request, 'shop/cart.html', {'user': request.user, 'cart': cart, 'recommended_products': recommended_products,})
    else:
        return render(request, 'shop/cart.html', {'user': None, 'cart': None})

def add_to_cart(request, name):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, name=name)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)

        # Create a UserInteraction instance for the 'added_to_cart' action
        UserInteraction.objects.create(user=request.user, action_type='added_to_cart', product=product)

        return redirect('shop:cart')
    else:
        return redirect('login')

def remove_from_cart(request, name):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, name=name)
        cart = get_object_or_404(Cart, user=request.user)
        cart.products.remove(product)
        return redirect('shop:cart')
    else:
        return redirect('login')  # Redirect to login page if the user is not authenticated

def filtered_products(request):
    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', '')
    order = request.GET.get('order', 'asc')

    products = Product.objects.all()

    # Filter by category if selected
    if selected_category:
        products = products.filter(category__name=selected_category)

    # Filter by search query if provided
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Apply sorting based on the selected option and order
    if sort_by == 'rating':
        products = products.order_by(f'{"-" if order == "desc" else ""}average_rating')
    elif sort_by == 'price':
        products = products.order_by(f'{"-" if order == "desc" else ""}price')

    categories = Category.objects.values_list('name', flat=True).distinct()

    context = {
        'objects': products,
        'categories': categories,
        'selected_category': selected_category,
        'sort_by': sort_by,
        'order': order,
    }

    return render(request, 'shop/filtered_products.html', context)

def get_viewed_products(user):
    viewed_products = UserInteraction.objects.filter(user=user, action_type='view')
    cart_products = UserInteraction.objects.filter(user=user, action_type='added_to_cart')

    viewed_product_ids = set(action.product.id for action in viewed_products)
    cart_product_ids = set(action.product.id for action in cart_products)

    return list(viewed_product_ids - cart_product_ids)

def get_recommendations(user, top_n=3):
    viewed_product_ids = get_viewed_products(user)
    recent_viewed_products = UserInteraction.objects.filter(user=user, action_type='view', product__id__in=viewed_product_ids).order_by('-timestamp')[:top_n]

    return [action.product for action in recent_viewed_products]

@login_required
def recommend_products(request):
    user = request.user
    recommended_products = get_recommendations(user)

    context = {
        'recommended_products': recommended_products,
    }

    return render(request, 'shop/recommended_products.html', context)

def rate_product(request, name):
    if request.method == 'POST':
        product = get_object_or_404(Product, name=name)
        rating_value = int(request.POST.get('rating', 0))

        # Check if the user has already rated this product
        existing_rating = Rating.objects.filter(product=product, user=request.user).first()
        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            Rating.objects.create(product=product, user=request.user, rating=rating_value)

        # Update the average rating for the product
        product.update_average_rating()

    return redirect('shop:productDetails', name=name)