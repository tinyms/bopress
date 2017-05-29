from rest_framework import serializers

from oauth2.models import UserInfo, CompanyInfo, CompanyEmployee, AppCommerceLicense, AppGrantAuthorization


class OAuth2VerifySerializer(serializers.Serializer):
    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance

    code = serializers.CharField(max_length=255, required=True)


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserInfo
        fields = ('union_id', 'nick_name', 'gender', 'city', 'province', 'country', 'avatar_url', 'app_id',
                  'mobile', 'name', 'address', 'identity_card', 'timestamp', 'user')


class CompanyInfoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.name')

    class Meta:
        model = CompanyInfo
        fields = ('company_name', 'name', 'mobile', 'logo', 'address', 'phone', 'summary', 'description', 'owner')


class CompanyEmployeeSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.company_name')
    employee_name = serializers.ReadOnlyField(source='employee.name')

    class Meta:
        model = CompanyEmployee
        fields = ('company', 'employee', 'level')


class AppCommerceLicenseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AppCommerceLicense
        fields = ('level', 'name', 'price', 'position')


class AppGrantAuthorizationSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.company_name')

    class Meta:
        model = AppGrantAuthorization
        fields = ('app_id', 'app_name', 'start_time', 'end_time', 'level', 'company')
