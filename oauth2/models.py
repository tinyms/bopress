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
