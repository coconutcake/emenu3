from rest_framework import serializers
from menu.models import Dish,Menu

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"
        

class MenuSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(many=True,queryset=Dish.objects.all())
    class Meta:
        model = Menu
        fields = "__all__"

    
class MenuListSerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True,read_only=True)
    class Meta:
        model = Menu
        fields = "__all__"
        
