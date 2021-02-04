from django.test import TestCase
import datetime
from django.forms.models import model_to_dict
from menu.models import Dish,Menu

# Fukcje pomocnicze
def get_current_datetime():
    return datetime.datetime.now()

class DishTests(TestCase):
    """ Testy modelu Product """
    def setUp(self):
        self.model = Dish
    def test_if_created_success(self):
        """ Testowanie utworzenia obiektu Dish przy podaniu poprawnych danych wejsciowych"""
        
        params_0 = {
            "name": "nazwa dania",
            "description": "jakis opis dania",
            "price":4.99,
            "etc":datetime.timedelta(days=0,hours=0,minutes=15),
            "is_vege":True
            }
        
        created = self.model.objects.create(**params_0)
        
        self.assertEqual(model_to_dict(created, fields=params_0.keys()),params_0)
        self.assertTrue(created.created)
        self.assertFalse(created.updated)
          
    def test_if_updated_success(self):
        """ Testowanie aktualizacji obiektu Menu przy podaniu poprawnych danych wejsciowych"""
        
        params_0 = {
            "name": "nazwa dania",
            "description": "jakis opis dania",
            "price":4.99,
            "etc":datetime.timedelta(days=0,hours=0,minutes=15),
            "is_vege":True
            }
        params_1 = {
            "name": "nazwa dania1",
            "description": "jakis opis dania1",
            "price":5.99,
            "etc":datetime.timedelta(days=0,hours=0,minutes=20),
            "is_vege":False
        }
        
        created = self.model.objects.create(**params_0)
        self.model.objects.filter(pk=created.pk).update(**params_1)
        updated = self.model.objects.get(pk=created.pk)
        
        self.assertEqual(model_to_dict(updated, fields=params_1.keys()),params_1)
        self.assertTrue(updated.updated)
        self.assertNotEqual(updated.created,updated.updated)
        
        
               
class MenuTests(TestCase):
    """ Testy modelu Product """
    def setUp(self):
        self.model = Menu
        dish = {
            "name": "nazwa dania",
            "description": "jakis opis dania",
            "price":4.99,
            "etc":datetime.timedelta(days=0,hours=0,minutes=15),
            "is_vege":True
            }
        self.dish = Dish.objects.create(**dish)
    def test_if_created_success(self):
        """ Testowanie utworzenia obiektu Menu przy podaniu poprawnych danych wejsciowych"""

        params_0 = {
            "name": "nazwa menu",
            }
        
        created = self.model.objects.create(**params_0)
        created.dish.add(self.dish)
        self.assertEqual(model_to_dict(created, fields=params_0.keys()),params_0)
        self.assertTrue(created.dish.exists())   

        
