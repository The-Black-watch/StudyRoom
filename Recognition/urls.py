from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = '[Recognition]'

urlpatterns = [
    # path('get_assignments/', views.get_assignments)
    url('resource', views.get_resource),
    url('detect', views.detect),
    # url(r'^start', views.start),
    url('startDetect', views.CamConfig.show_pic),
    url('getRoomName', views.getRoomName),
    url('exitRoom', views.exitRoom),
    url('enterRoom', views.enterRoom),
    
]
