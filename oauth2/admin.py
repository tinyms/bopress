from django.contrib import admin
from oauth2.models import UserInfo, CompanyInfo, CompanyEmployee, AppCommerceLicense, AppGrantAuthorization


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('open_id', 'union_id', 'nick_name', 'gender', 'city', 'province', 'country', 'mobile', 'name',
                    'address', 'identity_card', 'app_id', 'user')


class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'mobile', 'logo', 'address', 'phone', 'owner')


class CompanyEmployeeAdmin(admin.ModelAdmin):
    list_display = ('company', 'employee', 'level')


class AppCommerceLicenseAdmin(admin.ModelAdmin):
    list_display = ('level', 'name', 'price', 'position')


class AppGrantAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'app_name', 'start_time', 'end_time', 'level', 'company')


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(CompanyEmployee, CompanyEmployeeAdmin)
admin.site.register(AppCommerceLicense, AppCommerceLicenseAdmin)
admin.site.register(AppGrantAuthorization, AppGrantAuthorizationAdmin)
