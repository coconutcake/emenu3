from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives
from project.settings import EMAIL_HOST_USER

class EmailNotification():
    def __init__(self, *args, **kwargs):
        self.template = kwargs.get("template")
        self.request = kwargs.get("request",None)
        self.instance = kwargs.get("instance",None)
        self.emails = kwargs.get("emails",None)
        self.subject = kwargs.get("subject")
        self.set_mails = tuple()
    
    def get_render(self,context):
        print("Renderuje mail")
        return render_to_string(self.template, context)
    
    def set_mail(self,**kwargs):
        context = kwargs.get("context")
        render = self.get_render(context)
        email = kwargs.get("email")
        
        to_send = (
            self.subject,
            render,
            EMAIL_HOST_USER,
            [email]
            )     
        
        self.set_mails += ((to_send),)
    
    def send_all(self):
        print(f"Wysyłam masowy mailing...")       
        return True if send_mass_mail(self.set_mails) else False
        


        
        