from django.urls import path
from . import views
#from .views import add_to_cart, cart, remove_from_cart

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Namespace
app_name = 'shop'


urlpatterns = [
	path('', views.shop, name="shop"),
 	path('products/', views.products, name="products"),
  
    
    path('category/<slug:category_slug>/', views.category, name='category'),
    
    
    path('productDetails/<path:name>/', views.productDetails, name='productDetails'),
    
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<path:name>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<path:name>/', views.remove_from_cart, name='remove_from_cart'),






]

urlpatterns += staticfiles_urlpatterns()

