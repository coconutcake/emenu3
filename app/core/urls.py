from django.urls import path

from django.conf.urls import url
from core import views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

app_name = 'core'

urlpatterns = [
    # Email push
    url(r'email_push/$', csrf_exempt(views.CommandEmailPushView.as_view()),name='email_push'),

]