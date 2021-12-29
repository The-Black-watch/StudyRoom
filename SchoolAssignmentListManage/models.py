# -*- coding: UTF-8 -*-
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# 课程名
from django.utils import timezone

from SchoolAssignmentListManage.diy_widgets import ImageInput, UploadModel
from Course.models import Course, Student
from Course.models import Teacher


class ScheduleName(models.Model):
    # 科目名
    # schedule_name = models.CharField(max_length=50, choices=schedule_name_choice)
    schedule_name = models.CharField(max_length=50, verbose_name='课程名称', unique=True)

    class Meta:
        db_table = 'schedule_name'
        verbose_name = '课程'
        verbose_name_plural = "课程管理"

    def __str__(self):
        return self.schedule_name


class AssignmentInfo(models.Model):
    # 课程名
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程名称')

    # 作业信息
    assignmentInfo = models.CharField(verbose_name='作业内容', max_length=500)

    # 开始时间
    start_time = models.DateTimeField(verbose_name='开始时间', auto_now=False, default=timezone.now)
    # 结束时间
    end_time = models.DateTimeField(verbose_name='结束时间', auto_now=False, blank=True, null=True)

    # 补充信息
    additionalInfo = models.TextField(verbose_name='补充信息', blank=True, null=True, default=None)

    # 是否需要上传文件
    # is_need_upload_file = models.BooleanField(verbose_name='是否需要上传文件', default=False)

    # 文件
    file = models.FileField(verbose_name='文件', upload_to='file/', blank=True, null=True, default=None)

    # 图片
    image = models.ImageField(verbose_name='图片', upload_to='image/', blank=True, null=True, default=None)

    # images = forms.FileField(label="图片", widget=ImageInput, help_text="按住ctrl多选,最多4张", required=False)

    class Meta:
        # model = UploadModel
        verbose_name = '作业'
        verbose_name_plural = "作业管理111"


class Room(models.Model):
    # 自习室名
    Room_name = models.CharField(max_length=50, verbose_name='自习室名称', unique=True)
    # 自习室介绍
    introduction = models.CharField(max_length=250, verbose_name='简介')
    # 自习室类型
    type_choices = (
        (1, '专业课'),
        (2, '基础课'),
        (3, '课外兴趣课')
    )
    type = models.IntegerField(choices=type_choices, blank=True, null=True, verbose_name='类别')
    # 自习室拥有者
    owner = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='自习室老师', default=None)
    # 自习室人数
    number = models.IntegerField(verbose_name='自习室人数', default=0)

    class Meta:
        db_table = 'Room'
        verbose_name = '自习室'
        verbose_name_plural = "自习室管理"

    def __str__(self):
        return self.Room_name


class DistractionRecord(models.Model):
    # 学生
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生', default=None)
    # 自习室
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='自习室', default=None)
    # 分心行为
    distraction_choices = (
        (1, '玩手机'),
        (2, '抽烟'),
        (3, '喝水')
    )
    distraction_action = models.IntegerField(choices=distraction_choices, blank=True, null=True, verbose_name='分心行为')
    # 时间
    time = models.TimeField(verbose_name='分心时间')

    class Meta:
        db_table = 'DistractionRecord'
        verbose_name = '分心记录'
        verbose_name_plural = "分心记录管理"

    def __str__(self):
        return self.student.student_name
