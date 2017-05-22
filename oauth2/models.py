from django.db import models
from django.contrib.auth.models import User


class OAuth2(models.Model):
    open_id = models.CharField(max_length=255, verbose_name="OpenID")
    union_id = models.CharField(max_length=255, verbose_name="UnionID", blank=True, default="")
    nick_name = models.CharField(max_length=255, verbose_name="昵称", blank=True, default="")
    gender = models.CharField(max_length=20, verbose_name="性别", blank=True, default="")
    city = models.CharField(max_length=30, verbose_name="城市", blank=True, default="")
    province = models.CharField(max_length=30, verbose_name="省份", blank=True, default="")
    country = models.CharField(max_length=20, verbose_name="国家", blank=True, default="")
    avatar_url = models.CharField(max_length=255, verbose_name="头像", blank=True, default="")
    app_id = models.CharField(max_length=255, verbose_name="AppID", blank=True, default="")
    timestamp = models.CharField(max_length=64, verbose_name="认证时间", blank=True, default="")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="用户")


# 公司基本信息
class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="公司名称")
    name = models.CharField(max_length=50, verbose_name="法人")
    mobile = models.CharField(max_length=20, verbose_name="手机号码")
    logo = models.CharField(max_length=255, verbose_name="LOGO", blank=True)
    address = models.CharField(max_length=255, verbose_name="公司注册地")
    phone = models.CharField(max_length=20, verbose_name="固定电话", blank=True)
    spread_mobile = models.CharField(max_length=20, verbose_name="推广人手机号码")
    summary = models.TextField(verbose_name="简介", blank=True, default="")
    description = models.TextField(verbose_name="场地描述", blank=True, default="")
    owner = models.ForeignKey(to=OAuth2, on_delete=models.CASCADE, verbose_name="认证用户")


# 教师
class Teacher(models):
    name = models.CharField(max_length=50, verbose_name="姓名")
    photo = models.CharField(max_length=255, verbose_name="照片", blank=True, default="")
    working_yeas = models.IntegerField(verbose_name="教龄", default=1)
    speciality = models.CharField(max_length=255, verbose_name="专业", default="")
    profile = models.TextField(verbose_name="简介", blank=True, default="")
    company = models.ForeignKey(to=CompanyInfo, on_delete=models.CASCADE, verbose_name="关联公司")


# Product Price
class SoftPrice(models.Model):
    # base, adv
    level = models.CharField(max_length="10", verbose_name="级别")
    name = models.CharField(max_length=255, verbose_name="级别名称")


# 授权时间
class AppGrantAuthorization(models.Model):
    app_id = models.CharField(max_length=255, verbose_name="AppID", blank=True, default="")
    app_name = models.CharField(max_length=255, verbose_name="AppName", blank=True, default="")
    start_time = models.DateTimeField(verbose_name='开始时间', null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True)
    # base 初级版 adv 高级版
    level = models.CharField(max_length="10", verbose_name="软件级别")
    company = models.ForeignKey(to=CompanyInfo, on_delete=models.CASCADE, verbose_name="关联公司")


# 课程
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名称")
    requirement = models.CharField(max_length=255, default="", verbose_name="招生要求", blank=True)
    num_limit = models.IntegerField(verbose_name="人数限制", default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    address = models.CharField(max_length=255, verbose_name="教学地址", default="", blank=True)
    photo = models.CharField(max_length=255, verbose_name="特色图片", blank=True, default="")
    description = models.TextField(verbose_name="课程描述", blank=True, default="")
    company = models.ForeignKey(to=CompanyInfo, on_delete=models.CASCADE, verbose_name="关联公司")
