
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView





urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('shop/', include('shop.urls')),
    path('register/', include('register.urls')),
    
    path('', include("django.contrib.auth.urls")),
    
    path("", TemplateView.as_view(template_name="home.html"), name="home"),



    

    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

