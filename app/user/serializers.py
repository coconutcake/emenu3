from django.contrib.auth import \
    get_user_model,authenticate
from django.utils.translation import \
    ugettext_lazy as _
from rest_framework import \
    serializers
from core.models import \
    User
from rest_framework.authtoken.models import \
    Token
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    password = serializers.CharField(\
        write_only=True,
        style={'input_type':'password'}
        )
    
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

    