from django.db import models
from django.contrib.auth.models import User


class OAuth2(models.Model):
    open_id = models.CharField(max_length=255, verbose_name="OpenID")
    union_id = models.CharField(max_length=255, verbose_name="UnionID")
    nick_name = models.CharField(max_length=255, verbose_name="昵称")
    gender = models.CharField(max_length=20, verbose_name="性别")
    city = models.CharField(max_length=30, verbose_name="城市")
    province = models.CharField(max_length=30, verbose_name="省份")
    country = models.CharField(max_length=20, verbose_name="国家")
    avatar_url = models.CharField(max_length=255, verbose_name="头像")
    app_id = models.CharField(max_length=255, verbose_name="AppID")
    timestamp = models.CharField(max_length=64, verbose_name="认证时间")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="用户")
