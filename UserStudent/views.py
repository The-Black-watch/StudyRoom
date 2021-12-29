import json

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from SchoolAssignmentListManage.models import Room, DistractionRecord
from Course.models import Student


# Create your views here.
def home(request):
    return render(request, "index.html")


def rooms(request):
    return render(request, "rooms.html")


def records(request):
    return render(request, "records.html")


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def participate(request):
    return render(request, "resource.html")


def resource(request):
    return render(request, "resource.html")


def tOInfo(request):
    return render(request, "myInfo.html")


def doLogin(request):
    json_data = json.loads(request.body)
    username = json_data.get("userName")
    password = json_data.get("password")
    if username and password:  # 确保用户名和密码都不为空
        try:
            user = Student.objects.get(user_name=username)
        except:
            return JsonResponse({'ret': 1, 'msg': "用户不存在"})
        if user.password == password:
            request.session['user_name'] = username
            return JsonResponse({'ret': 0, 'msg': "登录成功"})
        return JsonResponse({'ret': 1, 'msg': "密码错误"})
    return JsonResponse({'ret': 1, 'msg': "用户名和密码不能为空"})


def doRegister(request):
    json_data = json.loads(request.body)
    username = json_data.get("userName")
    password = json_data.get("password")
    rePassword = json_data.get("rePassword")
    if password == rePassword:
        same_name_user = Student.objects.filter(user_name=username)
        if same_name_user:
            return JsonResponse({'ret': 1, 'msg': "用户已存在"})
        new_user = Student()
        new_user.user_name = username
        new_user.password = password
        new_user.save()
        return JsonResponse({'ret': 0, 'msg': "注册成功"})
    return JsonResponse({'ret': 1, 'msg': "两次输入密码不一致"})


def listRooms(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    qs = Room.objects.values()
    json_data = json.loads(request.body)
    roomName = json_data.get("roomName")
    type = json_data.get("type")
    if roomName:
        qs = qs.filter(Room_name=roomName)
    if type and type != "0":
        qs = qs.filter(type=type)
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


def listDistractionRecords(request):
    qs = DistractionRecord.objects.values()
    qs = qs.filter(student_id=request.session.get('user_name'))
    json_data = json.loads(request.body)
    roomId = json_data.get("roomId")
    distraction = json_data.get("action")
    if roomId:
        qs = qs.filter(room_id=roomId)
    if distraction and distraction != "0":
        qs = qs.filter(distraction_action=distraction)
    retlist = list(qs)
    return JsonResponse({'ret': 0, 'retlist': retlist})


def info(request):
    user = Student.objects.get(user_name=request.session.get('user_name'))
    if user.gender == 1:
        genderType = "男"
    if user.gender == 2:
        genderType = "女"
    return JsonResponse({'ret': 0, 'studentName': user.student_name, 'age': user.age, 'gender': genderType, 'major': user.major})


def updateInfo(request):
    print(11111111111)
    json_data = json.loads(request.body)
    student_name = json_data.get("studentName")
    age = json_data.get("age")
    gender = json_data.get("gender")
    major = json_data.get("major")
    if gender == "男":
        genderType = 1
    if gender == "女":
        genderType = 2
    user = Student.objects.get(user_name=request.session.get('user_name'))
    user.student_name = student_name
    user.age = age
    user.gender = genderType
    user.major = major
    user.save()
    return JsonResponse({'ret': 0, 'msg': "更新成功"})
