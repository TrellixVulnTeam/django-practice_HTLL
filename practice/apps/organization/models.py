from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="城市名")
    desc = models.CharField(max_length=100, verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名")
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(max_length=20, choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")),
                                verbose_name="机构类别", default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    students = models.IntegerField(default=0, verbose_name="学习人数")

    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图")
    address = models.CharField(max_length=100, verbose_name="机构地址")
    city = models.ForeignKey(City, verbose_name="所在城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()  # 返回教师数


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="teacher/%Y/%m", default='', verbose_name="教师头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
