from rest_framework import serializers
from gluru_backend.utils import generate_hash
from profiles import models as m


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.User
        fields = (
            'id', 'first_name', 'last_name'
        )


class ShortCompanySerializer(serializers.ModelSerializer):

    admin_user = ShortUserSerializer(read_only=True)

    class Meta:
        model = m.Company
        fields = (
            'id', 'name', 'admin_user'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'token'
        )


class UserMembershipSerializer(serializers.ModelSerializer):

    company = ShortCompanySerializer(read_only=True)

    class Meta:
        model = m.Membership
        fields = (
            'company', 'role'
        )


class UserAssociationSerializer(serializers.ModelSerializer):

    associations = UserMembershipSerializer(
        source='membership_set', many=True, required=False
    )

    class Meta:
        model = m.User
        fields = (
            'id', 'associations'
        )


class CompanyMembershipSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = m.Membership
        fields = (
            'user', 'role'
        )


class CompanySerializer(serializers.ModelSerializer):

    users = CompanyMembershipSerializer(
        source='membership_set', many=True, required=False
    )

    class Meta:
        model = m.Company
        fields = (
            'id', 'name', 'users'
        )


class ChangeRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Membership
        fields = (
            'role',
        )
        extra_kwargs = {
            'role': {'allow_null': False}
        }


class InvitationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = m.Invitation
        fields = ['id', 'email', 'invited_by', 'company', 'role']

    def create(self, validated_data):
        invited_by = self.context.get('invited_by', None)
        company = self.context.get('company', None)
        activation_key = generate_hash(
            validated_data.get('email')
        )
        return m.Invitation.objects.create(
            invited_by=invited_by,
            company=company,
            activation_key=activation_key,
            **validated_data
        )


class PersonalProfileSerializer(serializers.Serializer):

    address = serializers.CharField()
    timezone = serializers.CharField()
    job_title = serializers.CharField()
    about = serializers.CharField()
