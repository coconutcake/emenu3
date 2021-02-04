from django.contrib import admin
from django.utils.translation import gettext as _
from menu.models import *

# Fukcje pomocnicze
def get_model_meta_fields(model,excluded=[]):
    return [field.name for field in model._meta.get_fields() if field.name not in excluded]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    readonly_fields = ["created","updated"]
    list_display = get_model_meta_fields(Menu,excluded=["id","dish"])

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    readonly_fields = ["created","updated"]
