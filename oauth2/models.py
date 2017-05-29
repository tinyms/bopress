from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserInfo(models.Model):
    open_id = models.CharField(max_length=255, verbose_name="OpenID", unique=True)
    union_id = models.CharField(max_length=255, verbose_name="UnionID", blank=True, default="")
    nick_name = models.CharField(max_length=255, verbose_name="昵称", blank=True, default="")
    gender = models.CharField(max_length=20, verbose_name="性别", blank=True, default="")
    city = models.CharField(max_length=30, verbose_name="城市", blank=True, default="")
    province = models.CharField(max_length=30, verbose_name="省份", blank=True, default="")
    country = models.CharField(max_length=20, verbose_name="国家", blank=True, default="")
    avatar_url = models.CharField(max_length=255, verbose_name="头像", blank=True, default="")
    app_id = models.CharField(max_length=255, verbose_name="AppID", blank=True, default="")
    timestamp = models.CharField(max_length=64, verbose_name="认证时间", blank=True, default="")
    mobile = models.CharField(max_length=20, verbose_name="手机号码", blank=True, default="")
    name = models.CharField(max_length=50, verbose_name="姓名", blank=True, default="")
    address = models.CharField(max_length=255, verbose_name="住址", blank=True, default="")
    identity_card = models.CharField(max_length=25, verbose_name="身份证", blank=True, default="")
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="用户", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        verbose_name = _("用户基本资料")
        verbose_name_plural = _('用户基本资料')

    def __str__(self):
        return self.nick_name


# 公司基本信息
class CompanyInfo(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="公司名称")
    name = models.CharField(max_length=50, verbose_name="法人")
    mobile = models.CharField(max_length=20, verbose_name="手机号码", unique=True)
    logo = models.CharField(max_length=255, verbose_name="LOGO", blank=True)
    address = models.CharField(max_length=255, verbose_name="公司注册地")
    phone = models.CharField(max_length=20, verbose_name="固定电话", blank=True)
    summary = models.TextField(verbose_name="简介", blank=True, default="")
    description = models.TextField(verbose_name="场地描述", blank=True, default="")
    owner = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name="认证用户", null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        verbose_name = _("公司基本信息")
        verbose_name_plural = _('公司基本信息')

    def __str__(self):
        return self.company_name


# 雇员
class CompanyEmployee(models.Model):
    company = models.ForeignKey(to=CompanyInfo, on_delete=models.CASCADE, verbose_name="公司", null=True)
    employee = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name="成员", null=True)
    level = models.CharField(max_length=10, choices=(('owner', '法人'), ('employee', '雇员')), default='employee')

    class Meta:
        verbose_name = _("雇员")
        verbose_name_plural = _('雇员')

    def __str__(self):
        return self.employee.nick_name


# 商业许可
class AppCommerceLicense(models.Model):
    # base, adv
    level = models.CharField(max_length=10, verbose_name="级别")
    name = models.CharField(max_length=255, verbose_name="级别名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    position = models.SmallIntegerField(verbose_name='排序', default=1)

    class Meta:
        verbose_name = _("商业许可")
        verbose_name_plural = _('商业许可')

    def __str__(self):
        return self.name


# 授权时间
class AppGrantAuthorization(models.Model):
    app_id = models.CharField(max_length=255, verbose_name="AppID")
    app_secret = models.CharField(max_length=255, verbose_name="AppSecret")
    app_name = models.CharField(max_length=255, verbose_name="AppName")
    start_time = models.DateTimeField(verbose_name='开始时间', null=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True)
    # base 初级版 adv 高级版
    level = models.CharField(max_length=10, verbose_name="软件级别")
    company = models.ForeignKey(to=CompanyInfo, on_delete=models.CASCADE, verbose_name="关联公司", null=True)

    class Meta:
        verbose_name = _("App授权")
        verbose_name_plural = _('App授权')

    def __str__(self):
        return self.company.company_name
