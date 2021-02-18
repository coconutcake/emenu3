from django.urls import path
from user import views
from rest_framework.routers import DefaultRouter


app_name = 'user'

urlpatterns = [
    path('list/', views.UserListView.as_view(),name='list'),
    path('create/', views.UserCreateView.as_view(),name='create'),
]
