from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', view=views.login, name=""),
    path('rooms.html', view=views.rooms, name="rooms"),
    path('records.html', view=views.records, name="records"),
    path('myInfo.html', view=views.tOInfo, name="myInfo"),
    path('toIndex', view=views.home, name="toIndex"),
    path('login', view=views.doLogin, name="login"),
    path('register', view=views.doRegister, name="register"),
    path('tpRegisterPage', view=views.register, name="tpRegisterPage"),
    path('listRooms', view=views.listRooms, name="listRooms"),
    path('listRecords', view=views.listDistractionRecords, name="listRecords"),
    path('getInfo', view=views.info, name="getInfo"),
    path('updateInfo', view=views.updateInfo, name="updateInfo"),
    path('participate', view=views.participate, name="participate"),
    url('resource', view=views.resource, name="resource"),
]
