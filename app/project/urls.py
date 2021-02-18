from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from django.urls import reverse


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@mign.pl"),
      license=openapi.License(name="BSD License"),
      
   ),
   public=True,
   url='https://127.0.0.1:4433/',
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # redirect "/" to swagger
    url(r'^$', RedirectView.as_view(url='/swagger/')),
    
    # admin urls
    path('accounts/', admin.site.urls),
    
    # api urls
    path('api/user/',include('user.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/menu/',include('menu.urls')),
    
    # curl commands urls
    path('commands/', include('core.urls')),
    
    # Swager urls
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
