from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
MY_TOKEN = reverse('user:mytoken')

def create_user(**params):
    return get_user_model().objects.create_user(**params)
def create_token(**params):
    user = get_user_model().objects.get(email=params.get("email"))
    return Token.objects.create(user=user)
class PublicUserApiTests(TestCase):
    """ Testy API user """
    def setUp(self):
        self.client = APIClient() 
    def test_create_valid_user_success(self):
        """ Testowanie tworzenia usera przy pomocy poprawnego payloadu """
        payload = {
            "email": "testowy@test.pl",
            "password": 'testpasswd',
            "name": "test name"
            }
        res = self.client.post(\
            CREATE_USER_URL,
            payload
            )
        self.assertEqual(\
            res.status_code, 
            status.HTTP_201_CREATED
            )
        user = get_user_model().objects.get(\
            **res.data
            )
        self.assertTrue(\
            user.check_password(payload['password'])
            )
        self.assertNotIn(\
            'password', 
            res.data
            ) 
    def test_user_exists(self):
        """ Testowanie czy user istnieje """
        payload = {
            "email": "testowy@test.pl",
            "password": 'testpasswd',
            "name": "test name"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    def test_password_too_short(self):
        """ Testowanie długosci hasła """
        payload = {
            "email": "testowy@test.pl",
            "password": 'tw',
            "name": "test name"
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
    def test_create_token_for_user(self):
        """ Test tworzenia tokena """
        payload = {
            "email":"test@test.pl",
            "password":"test123"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    def test_create_token_ivalid_credentials(self):
        """ Testuje czy jest token zostanie zwrocony przy podaniu blednych poświadczeń """
        payload_0 = {
            "email":"test@test.pl",
            "password":"test123"
        }
        create_user(**payload_0)
        payload_1 = {
            "email":"test1@test1.pl",
            "password":"test123"
        }
        res = self.client.post(TOKEN_URL,payload_1)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    def test_create_token_no_user(self):
        """ Testuje czy token nie został utworzony jesli user nie istnieje""" 
        payload = {
            "email":"test@test.pl",
            "password":"test123"
        }  
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    def test_create_token_no_password(self):
        """ Testuje tworzenie tokena bez podania hasła  """
        payload_0 = {
            "email": "test@test.pl",
            "password": "test123"
        }
        payload_1 = {
            "email": "test@test.pl",
        }
        create_user(**payload_0)
        res = self.client.post(TOKEN_URL,payload_1)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    def test_create_token_empty_password(self):
        """ Testuje tworzenie tokena przy podaniu pustego hasła """
        payload_0 = {
            "email": "test@test.pl",
            "password": "test123"
        }
        payload_1 = {
            "email": "test@test.pl",
            "password": ""
        }
        create_user(**payload_0)
        res = self.client.post(TOKEN_URL,payload_1)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

 
class PrivateUserApiTests(TestCase):
    """ Testy APi wymagające authentifikacji """
    def setUp(self):
        self.payload_0 = {
            "email": "test@test.pl",
            "password": "password",
            "name": "test123"
        }
        self.user = create_user(**self.payload_0)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  
    def test_retrieve_profile_success(self):
        """ Testuje czy można pobrać profil usera """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            "name":self.user.name,
            "email":self.user.email            
        })
    def test_retrieve_not_assigned_self_token(self):
        res = self.client.get(MY_TOKEN)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    def test_retrive_assigned_self_token(self):
        token = create_token(**self.payload_0) 
        res =self.client.get(MY_TOKEN)
        self.assertIn('key',res.data)
    def test_post_me_not_allowed(self):
        """ Testuje czy POST nie jest prawidłowym zapytaniem dla widoku """
        res = self.client.post(ME_URL,{})
        self.assertEqual(\
            res.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
            )    
    def test_update_user_profile(self):
        """ Testuje update/patch usera dla zalogowanego uzytkownika """
        payload_0 = {
            "name": "new_name",
            "password": "test123"
            }
        res = self.client.patch(ME_URL,payload_0)
        self.user.refresh_from_db()
        self.assertEqual(\
            self.user.name,
            payload_0['name']
            )
        self.assertTrue(\
            self.user.check_password(payload_0['password'])
            )
        self.assertEqual(\
            res.status_code,
            status.HTTP_200_OK
            )
        
        