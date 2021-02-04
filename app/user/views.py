from rest_framework import \
    generics,authentication,permissions
from rest_framework.authtoken.views import \
    ObtainAuthToken
from rest_framework.settings import \
    api_settings
from rest_framework.authtoken.models import \
    Token
from user.serializers import \
    UserSerializer,AuthTokenSerializer,UserTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Tworzy nowego usera w systemie """
    serializer_class = UserSerializer
    

class CreateTokenView(ObtainAuthToken):
    """ Widok tworzenia tokena """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES


class GetRequestedUserTokenView(generics.RetrieveAPIView):
    """ Widok tokena zalogowanego użytkownika """
    serializer_class = UserTokenSerializer
    def get_object(self):
        """ Zwraca instancje zalogowanego usera """
        return self.request.user
    
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Menadzer zalogowanego usera """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """ Zwraca instancje zalogowanego usera do serializera """
        return self.request.user


    
