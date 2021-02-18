from rest_framework import \
    generics,authentication,permissions
from rest_framework.settings import \
    api_settings
from rest_framework.generics import \
    ListCreateAPIView,CreateAPIView,ListAPIView
from core.models import \
    User
from rest_framework.permissions import \
    IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.authentication import \
    SessionAuthentication, BasicAuthentication, TokenAuthentication

from user.serializers import *
from rest_framework.response import Response
from rest_framework import status

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self,request,*args,**kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self,serializer):
        serializer.save()
        
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(\
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
            )



    
