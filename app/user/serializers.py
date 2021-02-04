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

class UserSerializer(serializers.ModelSerializer):
    """ Serializer dla userów """
    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'name'
            )
        extra_kwargs = {
            "password":
                {
                    "write_only":True,
                    'min_length':5
                }
            }
    def create(self, validated_data):
        """ Tworzy nowego usera """
        return get_user_model().objects.\
            create_user(**validated_data)
    def update(self,instance,validated_data):
        """ Updatuje usera i zwraca """
        password = validated_data.pop('password',None)
        user = super().update(instance,validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer dla authentyfikacji obiektu usera """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    
    def validate(self,attrs):
        """ Walidacja authentyfikacji usera przy użyciu przesłanych danych """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("Nie można zalogować przy użyciu dostarczonych danych")
            raise serializers.ValidationError(msg,code='authentification')
        attrs['user'] = user
        return attrs
        
    
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token

    def to_representation(self,instance):
        """ Odbiera instacje z widoku i zwraca token """
        try:
            payload = UserTokenSerializer.Meta.model.objects.get(\
                user=instance
                )
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"detail":"no token assigned"})
            #return {"error": "brak tokena"} 
        return model_to_dict(payload,fields=["key"])  