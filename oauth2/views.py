import requests
from aboutconfig import get_config
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from oauth2.models import OAuth2
from oauth2.serializers import OAuth2VerifySerializer, OAuth2Serializer
from oauth2.permissions import IsOwner


class WeXinApiView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format=None):
        serializer = OAuth2VerifySerializer(data=request.data)
        if serializer.is_valid():
            host = 'http://{}/api-token-auth'.format(request.stream.META['HTTP_HOST'])
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
                    u = User()
                    u.username = r['openid']
                    u.set_password(r['session_key'])
                    u.save()
                    # link wechat oauth2
                    o = OAuth2()
                    o.open_id = u.username
                    o.user = u
                    o.app_id = appid
                    o.save()
                    # make jwt
                    token_r = requests.post(host, data={'username': u.username, 'password': r['session_key']})
                    return Response(token_r, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Oauth2ViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = OAuth2.objects.all()
    serializer_class = OAuth2Serializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner,)
