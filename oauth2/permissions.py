from django.core.cache import cache
from rest_framework import permissions
from django.utils import timezone

from oauth2.models import AppGrantAuthorization, CompanyEmployee, UserInfo


def get_company_by_app_id(app_id_):
    """
    得到企业ID
    :param app_id_: 
    :return: company id
    """
    if not app_id_:
        return None
    company_ = cache['oauth2_company_app_{}'.format(app_id_)]
    if company_:
        return company_
    company_ = AppGrantAuthorization.objects.filter(app_id=app_id_) \
        .filter(end_time__gte=timezone.now()).values_list('company').first()
    if company_:
        cache['oauth2_company_app_{}'.format(app_id_)] = company_[0]
        return company_[0]
    return None


def get_company_by_user_id(user_id_):
    """
    得到企业ID
    :param user_id_: 
    :return: company id
    """
    if not user_id_:
        return None
    company_ = cache['oauth2_company_user_{}'.format(user_id_)]
    if company_:
        return company_
    company_ = CompanyEmployee.objects.filter(employee__user__id=user_id_).values_list('company').first()
    if company_:
        cache['oauth2_company_user_{}'.format(user_id_)] = company_[0]
        return company_[0]
    return None


def get_userinfo_by_user_id(user_id_):
    if not user_id_:
        return None
    userinfo = cache['oauth2_company_userinfo_{}'.format(user_id_)]
    if userinfo:
        return userinfo
    userinfo = UserInfo.objects.filter(user__id=user_id_).values_list('id').first()
    if userinfo:
        cache['oauth2_company_userinfo_{}'.format(user_id_)] = userinfo[0]
        return userinfo[0]
    return None


# 直接判断用户关联的数据
class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# 管理公司基本资料或者可以只读
class IsCompanyInfoOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.id == get_company_by_app_id(request.data['appid'])
        return obj.owner.id == get_userinfo_by_user_id(request.user.id)


# 查看此公司下的业务内容或者仅限拥有者或者管理员去修改
class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            company_id = get_company_by_app_id(request.data['appid'])
            if not company_id:
                return False
            return obj.company.id == company_id
        company_id = get_company_by_user_id(request.user.id)
        if not company_id:
            return False
        return obj.company.id == company_id
