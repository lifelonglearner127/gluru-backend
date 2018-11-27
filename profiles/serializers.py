from rest_framework import serializers
from profiles.models import User, Company, Membership


class ShortCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'name',
        )


class UserSerializer(serializers.ModelSerializer):
    companies = ShortCompanySerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'token', 'companies'
        )


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name'
        )


class MembershipSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = (
            'user', 'role'
        )


class CompanySerializer(serializers.ModelSerializer):

    users = MembershipSerializer(
        source='membership_set', many=True, required=False
    )

    class Meta:
        model = Company
        fields = (
            'name', 'users'
        )
