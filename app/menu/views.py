from django.shortcuts import render
from rest_framework import \
    generics,authentication,permissions
from rest_framework.settings import \
    api_settings
from menu.models import Dish,Menu
import json
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views import View
import django_filters.rest_framework
from menu.serializers import \
    DishSerializer, MenuSerializer, MenuListSerializer
from menu.filters import MenuFilterSet
from drf_yasg.utils import swagger_auto_schema

API_COMMENTS = {
    "create": "Tworzy nowy obiekt",
    "get": "Zwraca instancje obiektu",
    "put": "Edytuje pola instacji",
    "delete": "Usuwa instancje obiektu",
    "patch": "Czesciowo edytuje pola instancji"
}

class DishCreateView(generics.CreateAPIView):
    model = Dish
    serializer_class = DishSerializer
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("create"),
        operation_summary="",
        )
    def post(self,request,*args,**kwargs):
        return super().post(request,*args,**kwargs)
    
    
class DishDetailView(generics.RetrieveUpdateAPIView):
    
    model = Dish
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("put"),
        operation_summary="",
        )
    def put(self,request,*args,**kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("put"),
        operation_summary="",
        )
    def patch(self,request,*args,**kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get"),
        operation_summary="",
        )
    def get(self,request,*args,**kwargs):
        return super().get(request, *args, **kwargs)
        
    
class DishDeleteView(generics.DestroyAPIView):
    
    model = Dish
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("delete"),
        operation_summary="",
        )
    def delete(self,request,*args,**kwargs):
        return super().delete(request, *args, **kwargs)


class MenuCreateView(generics.CreateAPIView):
    model = Menu
    serializer_class = MenuSerializer
    
   
    def perform_create(self,serializer):
        return serializer.save()
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("create"),
        operation_summary="",
        )    
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create(serializer)
        listowane = MenuListSerializer(created)
        headers = self.get_success_headers(serializer.data)
        return Response(
            listowane.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        
        
class MenuDetailView(generics.RetrieveUpdateAPIView):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer
   
    def retrieve(self,request,pk=None):
        queryset = Menu.objects.all()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = MenuListSerializer(obj)

        return Response(\
            serializer.data,
            )
      
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("put"),
        operation_summary="",
        )
    def put(self,request,*args,**kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("patch"),
        operation_summary="",
        )
    def patch(self,request,*args,**kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get"),
        operation_summary="",
        )
    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args, **kwargs)    
      
       
class MenuDeleteView(generics.DestroyAPIView):
    model = Menu
    queryset = model.objects.all()
    serializer_class = MenuSerializer
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("delete"),
        operation_summary="",
        )
    def delete(self,request,*args,**kwargs):
        return super().delete(request, *args, **kwargs)
    
    
class MenuListView(generics.ListAPIView):
    
    model = Menu
    dishes = Dish.objects.all()
    queryset = model.objects.filter(dish__in=dishes).distinct()
    
    # Filtrowanie
    # filterset_fields = {
    #     "name":["icontains"],
    #     "created":["date"],
    #     "updated":["date"]
    #     }
    filterset_class = MenuFilterSet
    
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields = ['name']
    serializer_class = MenuListSerializer
    permission_classes = [
        permissions.AllowAny
        ]
    
    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get"),
        operation_summary="",
        )
    def get(self,request,*args,**kwargs):
        return super().list(request, *args, **kwargs)
  
    
class DishListView(generics.ListAPIView):
    model = Dish
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [
        permissions.AllowAny
        ]

    @swagger_auto_schema(\
        tags=[model.__name__],
        operation_description=API_COMMENTS.get("get"),
        operation_summary="",
        )
    def get(self,request,*args,**kwargs):
        return super().list(request, *args, **kwargs)
