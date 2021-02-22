import django_filters
from menu.models import Menu
from django.forms.widgets import TextInput

class MenuFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(\
        field_name="name",
        lookup_expr="icontains"
        )
    
    created = django_filters.DateTimeFilter(\
        field_name="created", 
        lookup_expr="date",
        label="Data utworzenia",
        widget=TextInput(attrs={'placeholder': 'ex. 2020-01-28'})
        )
        
    updated = django_filters.DateTimeFilter(\
        field_name="updated", 
        lookup_expr="date",
        label="Data aktualizacji",
        widget=TextInput(attrs={'placeholder': 'ex. 2020-01-28'})
        )
   
    class Meta:
        model = Menu
        fields = ["name","created","updated"]