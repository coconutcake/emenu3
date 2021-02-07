from django.test import TestCase
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives
from project.settings import EMAIL_HOST_USER
from core.additionals.emailnotify import EmailNotification
import unittest


class EmailNotificationCase(TestCase):
    def setUp(self):
        self.subject = "Test"
        self.template = "core/email_raw.html"
        self.cls = EmailNotification(
            template=self.template,
            subject=self.subject
        )
        
    def test_if_rendered(self):
        """ Testuje czy poprawnie renderuje context w template """
        context = {"instance":"instance"}
        render = self.cls.get_render(context)
        self.assertIn(context.get("instance"),render)

        
    def test_if_sent(self):
        """ Testuje czy wysyła mail """
        context = {}
        self.email = "no-reply@mign.pl" 
        self.cls.set_mail(
            context=context,
            email="no-reply@mign.pl"
        )
        self.assertTrue(self.cls.send_all())
