from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.views import *
import datetime
from menu.models import Dish,Menu
from rest_framework import status
from django.forms import model_to_dict
from rest_framework.test import force_authenticate

def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_token_for(instance):
    user = get_user_model().objects.get(email=instance.email)
    return Token.objects.create(user=user)

def get_user(**params):
    return get_user_model().objects.get(**params)

CREATE_USER_URL = "user:create"
LIST_USER_URL = "user:list"

class UserCreateViewCase(TestCase):
    def setUp(self):
        self.client_superuser = APIClient()
        self.payload_0 = {
            "email": "test@test.pl",
            "password": "password",
            "name": "test123",
            "is_staff": True,
            "is_superuser": True,
        }
        self.payload_1 = {
            "email": "teste@test.pl",
            "password": "passworde",
            "name": "test123e",
            "is_superuser": False,
        }
        self.superuser = create_user(**self.payload_0)
        self.user = create_user(**self.payload_1)
        self.client_superuser.force_authenticate(user=self.superuser)
        self.client_not_authenticated = APIClient()
        self.client_authenticated = APIClient()
        self.client_authenticated.force_authenticate(user=self.user)
    
        
    def test_if_created_superusers_permissions(self):
        """ Sprawdza czy uzytkownik is_staff moze dodac usera """
        payload = {
            "email": "t@t.pl",
            "password": "password",
            "name": "asdasd",
            "is_superuser": False,
        }

        res = self.client_superuser.post(reverse(CREATE_USER_URL),data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
    def test_if_not_created_authenticated_permissions(self):
        """ Sprawdza czy zabronione jest dodanie nowego uzytkownika przez zalogowanego usera """
        payload = {
            "email": "t@t.pl",
            "password": "password",
            "name": "asdasd",
            "is_superuser": False,
        }

        res = self.client_authenticated.post(reverse(CREATE_USER_URL),data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_if_not_created_unauthorized(self):
        """ Sprawdza czy uzyskownik niezalogowany nie moze dodac usera """
        payload = {
            "email": "t@t.pl",
            "password": "password",
            "name": "asdasd",
            "is_superuser": False,
        }

        res = self.client_not_authenticated.post(reverse(CREATE_USER_URL),data=payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        

class UserListViewCase(TestCase):
    
    def setUp(self):
        self.not_authenticated = APIClient()
        self.client_superuser = APIClient()
        self.client_authenticated = APIClient()
        payload = {
            "email": "test@test.pl",
            "password": "password",
            "name": "test123",
            "is_staff": True,
            "is_superuser": True,
        }
        payload_1 = {
            "email": "tccdesct@tcccest.pl",
            "password": "padcdccssword",
            "name": "tesscccdt123",
            "is_staff": False,
            "is_superuser": False,
        }
        self.superuser = create_user(**payload)
        self.authenticated = create_user(**payload_1)
        self.client_superuser.force_authenticate(user=self.superuser)
        self.client_authenticated.force_authenticate(user=self.authenticated)
        
    def test_if_allowed_for_superusers_permissions(self):
        """ Sprawdza czy lista jest dostepna dla is_staff """
        res = self.client_superuser.get(reverse(LIST_USER_URL),data={})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_if_forbiden_for_authenticated_permissions(self):
        """ Sprawdza czy lista nie jest dostepna dla uzytkownikow """
        res = self.client_authenticated.get(reverse(LIST_USER_URL),data={})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_if_not_available_for_unauthorized(self):
        """ Sprawdza czy dla nieagowanych endpoint jest niedostepny """
        res = self.not_authenticated.get(reverse(LIST_USER_URL),data={})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)