from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Namespace
app_name = 'shop'


urlpatterns = [



    path('', views.HomeView.as_view(), name='home'),

    path('products/', views.products, name="products"),

    path('filtered_products/', views.filtered_products, name='filtered_products'),
    
    path('recommend/', views.recommend_products, name='recommend_products'),

    path('rate-product/<slug:name>/', views.rate_product, name='rate_product'),
    
    path('productDetails/<path:name>/', views.productDetails, name='productDetails'),
    
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<path:name>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<path:name>/', views.remove_from_cart, name='remove_from_cart'),


]

urlpatterns += staticfiles_urlpatterns()

