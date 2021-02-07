from django.shortcuts import render
from rest_framework import \
    generics,authentication,permissions
from rest_framework.settings import \
    api_settings
from menu.models import Dish,Menu
import json
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views import View
import django_filters.rest_framework
from menu.serializers import \
    DishSerializer, MenuSerializer, MenuListSerializer

class DishCreateView(generics.CreateAPIView):
    serializer_class = DishSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]
  
    
class DishDetailView(generics.RetrieveUpdateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]
        
    
class DishDeleteView(generics.DestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]


class MenuCreateView(generics.CreateAPIView):
    serializer_class = MenuSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]
  
    
class MenuDetailView(generics.RetrieveUpdateAPIView):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]
    
   
    def retrieve(self,request,pk=None):
        queryset = Menu.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = MenuListSerializer(obj)
        return Response(serializer.data)
      
        
class MenuDeleteView(generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication
        ]
    permission_classes = [
        permissions.IsAuthenticated
        ]
  
    
class MenuListView(generics.ListAPIView):
    dishes = Dish.objects.all()
    queryset = Menu.objects.filter(dish__in=dishes).distinct()
    filterset_fields = {
        "name":["icontains"],
        "created":["icontains"],
        "updated":["icontains"]
        }
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['name']
    serializer_class = MenuListSerializer
    permission_classes = [
        permissions.AllowAny
        ]
  
    
class DishListView(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [
        permissions.AllowAny
        ]


