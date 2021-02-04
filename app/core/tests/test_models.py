from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

# USER
class UserTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Testy tworzenia usera """
        email = 'test@test.pl'
        password = 'Testpasswd123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )           
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_email_normalized(self):
        email = 'test@TEST.pl'
        user = get_user_model().objects.create_user(email,'test234')
        self.assertEqual(user.email,email.lower())
    def test_new_user_invaid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,"Test123")
    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@test.pl',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    def test_create_new_staffuser(self):
        email='worker@test.pl'
        password='test123'
        user = get_user_model().objects.create_staff(email,password)
        self.assertTrue(user.is_staff)

