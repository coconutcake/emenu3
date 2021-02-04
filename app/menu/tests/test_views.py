from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.forms import model_to_dict
import json
from menu.models import *
import datetime

# Widoki

# Dish
CREATE_DISH_URL = "menu:dish_create"
DETAIL_DISH_URL = "menu:dish_detail"
DELETE_DISH_URL = "menu:dish_delete"

# Menu
CREATE_MENU_URL = "menu:menu_create"
DETAIL_MENU_URL = "menu:menu_detail"
DELETE_MENU_URL = "menu:menu_delete"
LIST_MENU_URL = "menu:menu_list"

# Fukcje pomocnicze
def create_user(**params):
    return get_user_model().objects.create_user(**params)

def get_pks_list(objects):
    return [x.pk for x in objects]

def get_token(user_instance):
    instance = get_user_model().objects.get(pk=user_instance.pk)
    return Token.objects.get(user=instance)

def create_token(user_instance):
    instance = get_user_model().objects.get(pk=user_instance.pk)
    return Token.objects.create(user=instance)


# Testy Private
class DishApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Dish
        self.user_payload = {
            "email": "test@test.pl",
            "password": "password",
            "name": "test123",
            "is_superuser": True,
            }
        self.user = create_user(**self.user_payload)
        self.token = create_token(self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user,token=self.token)
        self.create_payload = {
            "name": "testname",
            "description": "testowy opis",
            "price": 15.99,
            "etc": datetime.timedelta(days=0,hours=0,minutes=15),
            "is_vege":True
            }
        self.edited_payload = self.create_payload.copy()
        self.edited_payload["name"] = "inna nazwa testowa"
        
    def test_if_created_success(self):
        """ Testuje utworzenie przy uzyciu poprawych danych wejsciowych """
        
        res = self.client.post(
            reverse(CREATE_DISH_URL),
            data=self.create_payload
            )
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
    def test_if_endpoints_are_secured(self):
        """ Sprawdza czy endpointy CRUD sa zabezpieczone przed klientami Anonymous """
        
        not_authenticated = APIClient()
        
        # Create
        res = not_authenticated.post(\
            reverse(CREATE_DISH_URL),
            data=self.create_payload
            )
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        
        # Detail
        created = self.client.post(\
            reverse(CREATE_DISH_URL),
            data=self.create_payload
            )
        res = not_authenticated.get(\
            reverse(DETAIL_DISH_URL,kwargs={'pk': created.data.get("id")})
            )
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        
        # Delete
        res = not_authenticated.delete(\
            reverse(DETAIL_DISH_URL,kwargs={'pk': created.data.get("id")})
            )
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_if_detail_success(self):
        """ Sprawdza czy endpoint detail poprawnie wybiera instancje zapisana """
        
        res = self.client.post(\
            reverse(CREATE_DISH_URL),
            data=self.create_payload
            )        
        obj = self.client.get(\
            reverse(DETAIL_DISH_URL,kwargs={'pk': res.data.get("id")})
            )
        self.assertEqual(obj.status_code,status.HTTP_200_OK)
        self.assertEqual(\
            self.create_payload.get("name"),
            obj.data.get("name")
            )

    def test_if_detail_update_success(self):
        """ Sprawdza czy endpoint umożliwia edycje pola instancji """

        res = self.client.post(\
            reverse(CREATE_DISH_URL),data=self.create_payload
            )
        edited = self.client.put(\
            reverse(DETAIL_DISH_URL,kwargs={'pk': res.data.get("id")}),
            data=self.edited_payload
            )
        self.assertEqual(edited.status_code,status.HTTP_200_OK)
        self.assertEqual(\
            self.edited_payload.get("name"),edited.data.get("name")
            )     
    
    def test_if_delete_success(self):
        """ Sprawdza czy endpoint umożliwia usuwanie instancji """
        
        res = self.client.post(\
            reverse(CREATE_DISH_URL),data=self.create_payload
            )
        deleted = self.client.delete(\
            reverse(DELETE_DISH_URL,kwargs={'pk': res.data.get("id")})
            )
        self.assertEqual(deleted.status_code,status.HTTP_204_NO_CONTENT)

        
class MenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Menu
        self.user_payload = {
            "email": "test@test.pl",
            "password": "password",
            "name": "test123",
            "is_superuser": True,
            }
        
        dish_1 ={
            "name": "testname",
            "description": "testowy opis",
            "price": 15.99,
            "etc": datetime.timedelta(days=0,hours=0,minutes=15),
            "is_vege":True
            }
        dish_2 ={
            "name": "testname2",
            "description": "testowy opis2",
            "price": 13.99,
            "etc": datetime.timedelta(days=0,hours=0,minutes=25),
            "is_vege":False
            }
        
        self.user = create_user(**self.user_payload)
        self.token = create_token(self.user)
        
        Dish.objects.create(**dish_1)
        Dish.objects.create(**dish_2)
        
        self.dishes = Dish.objects.all()
        
        self.create_payload = {
            "name": "nazwa menu",
            "dish":get_pks_list(self.dishes)
            }
        self.edited_payload = self.create_payload.copy()
        self.edited_payload["name"] = "inna nazwa testowa menu"
        self.client = APIClient()
        self.client.force_authenticate(user=self.user,token=self.token)        
        
    def test_if_created_success(self):
        """ Testuje utworzenie przy uzyciu poprawych danych wejsciowych """
    
        res = self.client.post(\
            reverse(CREATE_MENU_URL),
            data=self.create_payload
            )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.get(pk=res.data.get("id")))
        
    def test_if_endpoints_are_secured(self):
        """ Sprawdza czy endpoint jest zabezpieczony przed klientami Anonymous """

        not_authenticated = APIClient()
        
        # Create
        res = not_authenticated.post(\
            reverse(CREATE_MENU_URL),
            data=self.create_payload
            )
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

        # Detail
        created = self.client.post(\
            reverse(CREATE_MENU_URL),
            data=self.create_payload
            )
        res = not_authenticated.get(\
            reverse(DETAIL_MENU_URL,kwargs={'pk': created.data.get("id")})
            )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Delete
        res = not_authenticated.delete(\
            reverse(DELETE_MENU_URL,kwargs={'pk': created.data.get("id")})
            )
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
          
    def test_if_detail_success(self):
        """ Sprawdza czy endpoint detail poprawnie wybiera instancje zapisana """
        
        res = self.client.post(\
            reverse(CREATE_MENU_URL),
            data=self.create_payload
            )        
        obj = self.client.get(\
            reverse(DETAIL_MENU_URL,kwargs={'pk': res.data.get("id")})
            )
        self.assertEqual(obj.status_code,status.HTTP_200_OK)
        self.assertEqual(\
            self.create_payload.get("name"),obj.data.get("name"))

    def test_if_detail_update_success(self):
        """ Sprawdza czy endpoint umożliwia edycje pola instancji """

        res = self.client.post(\
            reverse(CREATE_MENU_URL),data=self.create_payload)
        edited = self.client.put(\
            reverse(DETAIL_MENU_URL,kwargs={'pk': res.data.get("id")}),
            data=self.edited_payload
            )
        self.assertEqual(edited.status_code,status.HTTP_200_OK)
        self.assertEqual(\
            self.edited_payload.get("name"),edited.data.get("name"))     
    
    def test_if_delete_success(self):
        """ Sprawdza czy endpoint umożliwia usuwanie instancji """
        
        res = self.client.post(\
            reverse(CREATE_MENU_URL),data=self.create_payload
            )
        deleted = self.client.delete(\
            reverse(DELETE_MENU_URL,kwargs={'pk': res.data.get("id")})
            )
        self.assertEqual(deleted.status_code,status.HTTP_204_NO_CONTENT)


# Testy Public
class PublicMenuApiTest(TestCase):
    def setUp(self):
        self.not_authenticated = APIClient()
        
    def test_if_endpoints_are_public(self):
        """ Sprawdza czy endpointy sa dostepne dla uzytkownika Anonymous """
        
        res = self.not_authenticated.get(reverse(LIST_MENU_URL))
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    
    