from rest_framework import serializers
from info.models import (
    GluuServer, GluuOS, GluuProduct, TicketCategory, TicketIssueType
)


class GluuServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GluuServer
        fields = '__all__'


class GluuOSSerializer(serializers.ModelSerializer):

    class Meta:
        model = GluuOS
        fields = '__all__'


class GluuProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = GluuProduct
        fields = '__all__'


class TicketCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketCategory
        fields = '__all__'


class TicketIssueTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketIssueType
        fields = '__all__'
