from django.contrib import admin
from oauth2.models import OAuth2


class OAuth2Admin(admin.ModelAdmin):
    list_display = ('open_id', 'union_id', 'nick_name', 'gender', 'city', 'province', 'country', 'app_id', 'user')


admin.site.register(OAuth2, OAuth2Admin)
