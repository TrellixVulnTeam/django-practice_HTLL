# _*_ coding:utf-8 _*_
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")  # 富文本编辑
    teacher = models.ForeignKey(Teacher, verbose_name="授课教师", null=True, blank=True)
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2, verbose_name="等级")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="web开发")
    tag = models.CharField(max_length=10, default="", verbose_name="课程标签")  # 关键词，用于相关课程的推荐
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    you_need_know = models.CharField(max_length=200, verbose_name="课程须知", default="")
    teacher_tell = models.CharField(max_length=200, verbose_name="老实告诉你将学会", default="")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):

        # 获取调用所有章节数

        return self.lesson_set.all().count()  # 反向读取全部的Lesson数，可以在前端直接调用

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]  # 反向读取某课程的学习用户（原型定义在operation中），取前5个，注意这里无需将operation
                                              # 中的UserCourse import到这里

    def get_course_lessons(self):
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    url = models.CharField(max_length=200, default="", verbose_name="访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=20, verbose_name="视频名")
    address = models.URLField(default="", verbose_name="访问地址")
    play_times = models.IntegerField(default=0, verbose_name="时长（分钟数）")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    name = models.CharField(max_length=20, verbose_name="名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    course = models.ForeignKey(Course, verbose_name="课程名")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="课程资源", max_length=100)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
