# 主函数
import sys
import os
from glob import glob
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from PySide2.QtCore import QDir, QTimer, Slot
from PySide2.QtGui import QPixmap, QImage
import cv2
import myframe
import numpy as np
from django.shortcuts import *
from django.http import HttpResponse, JsonResponse
import json
import base64
import numpy
from datetime import datetime
from SchoolAssignmentListManage import models

# 定义变量


# 初始化flag
init_flag = 1

# 循环次数
circle = 1  # 首次循环为1

# 循环周期
CIRCLE_CYCLE = 2  # 一个周期7张照片

# 眼睛闭合判断
EYE_AR_THRESH = 0.15  # 眼睛长宽比
EYE_AR_CONSEC_FRAMES = 2  # 闪烁阈值

# 嘴巴开合判断
MAR_THRESH = 0.65  # 打哈欠长宽比
MOUTH_AR_CONSEC_FRAMES = 3  # 闪烁阈值

# 定义检测变量，并初始化
COUNTER = 0  # 眨眼帧计数器
TOTAL = 0  # 眨眼总数
mCOUNTER = 0  # 打哈欠帧计数器
mTOTAL = 0  # 打哈欠总数
ActionCOUNTER = 0  # 分心行为计数器器

# 疲劳判断变量
# Perclos模型
# perclos = (Rolleye/Roll) + (Rollmouth/Roll)*0.2
Roll = 0  # 整个循环内的帧技术
Rolleye = 0  # 循环内闭眼帧数
Rollmouth = 0  # 循环内打哈欠数


def get_resource(request):
    return render(request, 'resource.html')


def getRoomName(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        room_id = json_data.get("room_id")
        room = models.Room.objects.get(id=room_id)
        return JsonResponse({'roomName': room.Room_name})


def exitRoom(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        room_id = json_data.get("room_id")
        room = models.Room.objects.get(id=room_id)
        num = room.number-1
        models.Room.objects.filter(id=room_id).update(number=num)
        print("退出自习室")
        return JsonResponse({"ret": 0})

        
def enterRoom(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        room_id = json_data.get("room_id")
        room = models.Room.objects.get(id=room_id)
        num = room.number+1
        models.Room.objects.filter(id=room_id).update(number=num)
        print("进入自习室")
        return JsonResponse({})


class Behavior:
    face = False  # 是否检测到人脸
    smoke = False
    phone = False
    drink = False
    tired = False
    yawn = 0

    def __init__(self):
        self.smoke = False
        self.phone = False
        self.drink = False
        self.tired = False
        self.yawn = 0


def createDistractionRecord(num, room_id, user_name):
    models.DistractionRecord.objects.create(distraction_action=num,
                                            time=datetime.now(),
                                            room_id=room_id, student_id=user_name)


# 定义摄像头类
class CamConfig:
    def __init__(self):

        print("")


    def show_pic(self, img_np, room_id, user_name):
        # 全局变量
        # 在函数中引入定义的全局变量
        global EYE_AR_THRESH, EYE_AR_CONSEC_FRAMES, MAR_THRESH, MOUTH_AR_CONSEC_FRAMES, CIRCLE_CYCLE, COUNTER, TOTAL, circle, mCOUNTER, mTOTAL, ActionCOUNTER, Roll, Rolleye, Rollmouth

        # print("Start Reading...")
        # 读取摄像头的一帧画面
        behavior = Behavior()
        # frame = cv2.imread('testData/test' + str(circle) + '.jpg', cv2.IMREAD_COLOR)
        frame = cv2.imdecode(img_np, 1)
        if isinstance(frame, np.ndarray):
            # Ui_MainWindow.printf(window, "获取成功" + 'testData/test' + str(circle) + '.jpg')
            circle = circle + 1
            if circle == CIRCLE_CYCLE:
                circle = 1
            success = True
        else:
            # Ui_MainWindow.printf(window, "获取失败" + 'testData/test' + str(circle) + '.jpg')
            success = False
        # success, frame = self.cap.read()
        if success:
            # 检测
            # 将摄像头读到的frame传入检测函数myframe.frametest()
            ret, frame = myframe.frametest(frame)
            lab, eye, mouth = ret
            print(ret[0])
            if len(ret[0]) != 0:
                if 'face' in ret[0] or 'drink' in ret[0]:
                    print("face detected!")
                    behavior.face = True
                    # ret和frame，为函数返回
                    # ret为检测结果，ret的格式为[lab,eye,mouth],lab为yolo的识别结果包含'phone' 'smoke' 'drink',eye为眼睛的开合程度（长宽比），mouth为嘴巴的开合程度
                    # frame为标注了识别结果的帧画面，画上了标识框

                    # 分心行为判断
                    # 分心行为检测以15帧为一个循环
                    ActionCOUNTER += 1

                    # 如果检测到分心行为
                    # 将信息返回到前端ui，使用红色字体来体现
                    # 并加ActionCOUNTER减1，以延长循环时间
                    for i in lab:
                        if i == "phone":
                            # window.label_6.setText("<font color=red>正在用手机</font>")
                            # window.label_9.setText("<font color=red>请不要分心</font>")
                            print("正在使用手机")
                            behavior.phone = True
                            createDistractionRecord('1', room_id, user_name)
                            if ActionCOUNTER > 0:
                                ActionCOUNTER -= 1
                        elif i == "smoke":
                            # window.label_7.setText("<font color=red>正在抽烟</font>")
                            # window.label_9.setText("<font color=red>请不要分心</font>")
                            print("正在抽烟")
                            behavior.smoke = True
                            createDistractionRecord('2', room_id, user_name)
                            if ActionCOUNTER > 0:
                                ActionCOUNTER -= 1
                        elif i == "drink":
                            # window.label_8.setText("<font color=red>正在喝水</font>")
                            # window.label_9.setText("<font color=red>请不要分心</font>")
                            print("正在喝水")
                            behavior.drink = True
                            createDistractionRecord('3', room_id, user_name)
                            if ActionCOUNTER > 0:
                                ActionCOUNTER -= 1

                    # 如果超过15帧未检测到分心行为，将label修改为平时状态
                    if ActionCOUNTER == 15:
                        # window.label_6.setText("手机")
                        # window.label_7.setText("抽烟")
                        # window.label_8.setText("喝水")
                        # window.label_9.setText("")
                        ActionCOUNTER = 0

                    # 疲劳判断
                    # 眨眼判断
                    if eye < EYE_AR_THRESH:
                        # 如果眼睛开合程度小于设定好的阈值
                        # 则两个和眼睛相关的计数器加1
                        COUNTER += 1
                        Rolleye += 1
                    else:
                        # 如果连续2次都小于阈值，则表示进行了一次眨眼活动
                        if COUNTER >= EYE_AR_CONSEC_FRAMES:
                            TOTAL += 1
                            # window.label_3.setText("眨眼次数：" + str(TOTAL))
                            # 重置眼帧计数器
                            COUNTER = 0

                    # 哈欠判断，同上
                    if mouth > MAR_THRESH:
                        mCOUNTER += 1
                        Rollmouth += 1
                    else:
                        # 如果连续3次都小于阈值，则表示打了一次哈欠
                        if mCOUNTER >= MOUTH_AR_CONSEC_FRAMES:
                            mTOTAL += 1
                            behavior.yawn += 1
                            # window.label_4.setText("哈欠次数：" + str(mTOTAL))
                            # 重置嘴帧计数器
                            mCOUNTER = 0

                    # 将画面显示在前端UI上
                    show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                    # window.label.setPixmap(QPixmap.fromImage(showImage))

                    # 疲劳模型
                    # 疲劳模型以150帧为一个循环
                    # 每一帧Roll加1
                    Roll += 1
                    # 当检测满150帧时，计算模型得分
                    if Roll == 150:
                        # 计算Perclos模型得分
                        perclos = (Rolleye / Roll) + (Rollmouth / Roll) * 0.2
                        # 在前端UI输出perclos值
                        # Ui_MainWindow.printf(window, "过去150帧中，Perclos得分为" + str(round(perclos, 3)))
                        # 当过去的150帧中，Perclos模型得分超过0.38时，判断为疲劳状态
                        if perclos > 0.38:
                            # Ui_MainWindow.printf(window, "当前处于疲劳状态")
                            # window.label_10.setText("<font color=red>疲劳！！！</font>")
                            # Ui_MainWindow.printf(window, "")
                            print("疲劳")
                            behavior.tired = True
                        else:
                            print("清醒")
                            behavior.tired = False
                            # Ui_MainWindow.printf(window, "当前处于清醒状态")
                            # window.label_10.setText("清醒")
                            # Ui_MainWindow.printf(window, "")

                        # 归零
                        # 将三个计数器归零
                        # 重新开始新一轮的检测
                        Roll = 0
                        Rolleye = 0
                        Rollmouth = 0
                        # Ui_MainWindow.printf(window, "重新开始执行疲劳检测...")
                else:
                    print("face not detected")
                    behavior.face = False
        return behavior


def CamConfig_init():
    # window.f_type = CamConfig()
    CamConfig()


def detect(request):
    global init_flag

    global EYE_AR_THRESH, EYE_AR_CONSEC_FRAMES, MAR_THRESH, MOUTH_AR_CONSEC_FRAMES, CIRCLE_CYCLE, COUNTER, TOTAL, circle, mCOUNTER, mTOTAL, ActionCOUNTER, Roll, Rolleye, Rollmouth

    print("detecting")
    if request.method == "POST":
        json_data = json.loads(request.body)
        str_image = json_data.get("imgData")
        room_id = json_data.get("room_id")
        user_name = request.session.get('user_name')
        img = base64.b64decode(str_image)
        img_np = numpy.fromstring(img, dtype='uint8')
        behavior = CamConfig().show_pic(img_np, room_id, user_name)

        circle = circle + 1
        if circle == CIRCLE_CYCLE:
            circle = 1
    return JsonResponse({'ret': 0,
                         'face': behavior.face,
                         'smoke': behavior.smoke,
                         'drink': behavior.drink,
                         'phone': behavior.phone,
                         'tired': behavior.tired,
                         'yawn': behavior.yawn})

