from django.urls import path

from django.conf.urls import url
from menu import views
from rest_framework.routers import DefaultRouter

app_name = 'menu'

urlpatterns = [
    # Dish
    url(r'dish/create/', views.DishCreateView.as_view(),name='dish_create'),
    url(r'dish/detail/(?P<pk>\d+)/$', views.DishDetailView.as_view(),name='dish_detail'),
    url(r'dish/delete/(?P<pk>\d+)/$', views.DishDeleteView.as_view(),name='dish_delete'),
    url(r'dish/list/', views.DishListView.as_view(),name='dish_list'),
    # Menu
    url(r'menu/create/', views.MenuCreateView.as_view(),name='menu_create'),
    url(r'menu/detail/(?P<pk>\d+)/$', views.MenuDetailView.as_view(),name='menu_detail'),
    url(r'menu/delete/(?P<pk>\d+)/$', views.MenuDeleteView.as_view(),name='menu_delete'),
    url(r'menu/list/', views.MenuListView.as_view(),name='menu_list'),
    
]
