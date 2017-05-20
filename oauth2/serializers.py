from rest_framework import serializers
from oauth2.models import OAuth2


class OAuth2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OAuth2
        fields = ('open_id', 'union_id', 'nick_name', 'gender', 'city', 'province', 'country', 'avatar_url', 'app_id',
                  'timestamp')
