from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.views import *
import datetime
from menu.models import Dish,Menu
from rest_framework import status

from project.settings import MASTER_TOKEN

EMAIL_PUSH_URL = "core:email_push"


class PomocniczeCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_current_time_instance(self):
        """ Testuje czy fukcja zwraca clase datetime z dzisiejsza datą"""
        current = get_current_time()
        now = datetime.datetime.now()
        self.assertTrue(isinstance(current,datetime.datetime))
        self.assertTrue(current.date,now.date)
        
    def test_yesterday_date_instance(self):
        """ Sprawdza czy zwracany jest dzien poprzedni """
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        instance = get_yesterday_date()
        self.assertTrue(yesterday.date,instance)
    
    def test_get_created_yesterdays_instance(self):
        """ Sprawdza czy zwraca obiekty utworzone z dnia poprzedniego """
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        
        dish_payload = {
            "name": "asdfasf",
            "description": "ssfwfwwerw",
            "price":12.99,
            "etc":"00:00:40",
            "is_vege":True
        }
        
        dish = Dish.objects.create(**dish_payload)
        dish.created = yesterday
        self.assertTrue(dish.created.date,yesterday.date)
        
    def test_get_updated_yesterdays_instance(self):
        """ Sprawdza czy zwraca obiekty zmodyfikowane z dnia poprzedniego """
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        
        dish_payload = {
            "name": "asdfasf",
            "description": "ssfwfwwerw",
            "price":12.99,
            "etc":"00:00:40",
            "is_vege":True
        }
        
        dish = Dish.objects.create(**dish_payload)
        dish.updated = yesterday
        self.assertTrue(dish.updated.date,yesterday.date)



