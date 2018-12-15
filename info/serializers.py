from rest_framework import serializers
from info import models as m


class GluuServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.GluuServer
        fields = '__all__'


class GluuOSSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.GluuOS
        fields = '__all__'


class GluuProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.GluuProduct
        fields = '__all__'


class TicketCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.TicketCategory
        fields = '__all__'


class TicketIssueTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.TicketIssueType
        fields = '__all__'


class TicketStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.TicketStatus
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Permission
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.UserRole
        fields = [
            'name', 'permissions'
        ]
