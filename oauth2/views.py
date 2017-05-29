import requests
from aboutconfig import get_config
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from django.db import transaction

from BoPress.log import Logger
from oauth2.models import UserInfo, CompanyInfo, CompanyEmployee, AppGrantAuthorization, AppCommerceLicense
from oauth2.permissions import IsOwner
from oauth2.serializers import OAuth2VerifySerializer, UserInfoSerializer, CompanyInfoSerializer, \
    CompanyEmployeeSerializer, AppGrantAuthorizationSerializer, AppCommerceLicenseSerializer


class WeXinApiView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        serializer = OAuth2VerifySerializer(data=request.data)
        if serializer.is_valid():
            host = 'http://{}/api-token-auth/'.format(request.stream.META['HTTP_HOST'])
            code = serializer.data.get('code', '')
            if code:
                appid = get_config('wechat.miniprogram.appid')
                secret = get_config('wechat.miniprogram.secret')
                query_params = '?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appid, secret,
                                                                                                     code)
                r = requests.get('https://api.weixin.qq.com/sns/jscode2session{}'.format(query_params)).json()
                if 'errcode' in r:
                    return Response(r, status=status.HTTP_400_BAD_REQUEST)
                # create a new user.
                try:
                    e_userinfo = UserInfo.objects.filter(open_id=r['openid']).first()
                    if not e_userinfo:
                        u = User()
                        with transaction.atomic():
                            u.username = r['openid']
                            u.is_active = True
                            u.is_staff = True
                            u.set_password(r['session_key'])
                            u.save()
                            # link wechat oauth2
                            e_userinfo = UserInfo()
                            e_userinfo.open_id = u.username
                            e_userinfo.user = u
                            e_userinfo.app_id = appid
                            e_userinfo.save()

                    else:
                        e_userinfo.user.set_password(r['session_key'])
                        e_userinfo.user.save()
                    # make jwt
                    token_r = requests.post(host, data={'username': r['openid'], 'password': r['session_key']}).json()
                    token_r['userinfo_id'] = e_userinfo.id
                    return Response(token_r, status=status.HTTP_200_OK)
                except Exception as e:
                    Logger.exception(e)
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class CompanyInfoCreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = ()

    def post(self, request, format=None):
        current_user = User.objects.get(request.user.id)
        user_info = UserInfo.objects.filter(user=current_user).first()
        if not user_info:
            return Response({"msg": 403}, status=status.HTTP_403_FORBIDDEN)
        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                ci = CompanyInfo(**serializer.data)
                ci.owner = user_info
                e = CompanyEmployee()
                e.company = ci
                e.employee = ci.owner
                e.level = "owner"
                current_user.email = request.data.get('email', '')
                ci.save()
                e.save()
                current_user.save()
            return Response({"company_id": ci.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyInfoViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        user_info = UserInfo.objects.get(user=self.request.user)
        serializer.save(owner=user_info)


class CompanyEmployeeViewSet(ReadOnlyModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = CompanyEmployee.objects.all()
    serializer_class = CompanyEmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AppCommerceLicenseViewSet(ReadOnlyModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = AppCommerceLicense.objects.all()
    serializer_class = AppCommerceLicenseSerializer
    permission_classes = ()
    authentication_classes = ()


class AppGrantAuthorizationViewSet(ReadOnlyModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = AppGrantAuthorization.objects.all()
    serializer_class = AppGrantAuthorizationSerializer
    permission_classes = (permissions.IsAuthenticated,)
