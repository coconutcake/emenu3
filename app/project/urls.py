from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('user.urls')),
   
    path('api/menu/',include('menu.urls')),
    path('commands/', include('core.urls')),

    
  

    
]
