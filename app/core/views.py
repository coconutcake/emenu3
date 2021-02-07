from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from project.settings import MASTER_TOKEN
import datetime
from menu.models import Menu,Dish
from core.models import User
from core.additionals.emailnotify import EmailNotification

# fukncje pomocnicze
def get_current_time():
    return datetime.datetime.now()
def get_yesterday_date():
    yesterday = get_current_time()-datetime.timedelta(days=1)
    return yesterday.date()
def get_created_yesterdays(model):
    return model.objects.filter(created__date=get_yesterday_date())
def get_updated_yesterdays(model):
    return model.objects.filter(updated__date=get_yesterday_date())
def get_key(request):
    key = json.loads(request.body).get("key")
    return key
def key_is_valid(request):
    if get_key(request) == MASTER_TOKEN[0]:
        return True
    return False

# Create your views here.
class CommandEmailPushView(View):
    email_template = "core/email_raw.html"
    model = User
    
    def get_context(self):
        context = {
            "created_yesterdays_menu":get_created_yesterdays(Menu),
            "updated_yesterdays_menu":get_updated_yesterdays(Menu),
        }
        return context
     
        
    def post(self, request, *args, **kwargs):
        context = self.get_context()

        self.notification = EmailNotification(\
            template=self.email_template,
            subject="Nowosci",
            )
        
        if key_is_valid(request):
            self.send_notify_to_all_users()
            return JsonResponse({})
        return JsonResponse({"msg":"invalid key"})


            
    def send_notify_to_all_users(self):
        for user in User.objects.all():
            context = self.get_context()
            context["instance"] = user
            
            self.notification.set_mail(
                context=context,
                email=user.email
            )
            
        self.notification.send_all()
            
