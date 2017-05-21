from rest_framework import serializers
from oauth2.models import OAuth2


class OAuth2VerifySerializer(serializers.Serializer):
    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance

    code = serializers.CharField(max_length=255, required=True)


class OAuth2Serializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = OAuth2
        fields = ('open_id', 'union_id', 'nick_name', 'gender', 'city', 'province', 'country', 'avatar_url', 'app_id',
                  'timestamp', 'user')
