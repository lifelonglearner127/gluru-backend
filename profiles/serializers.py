from django.conf import settings
from rest_framework import serializers
from gluru_backend.utils import generate_sha1
from profiles.models import User, Company, Membership, Invitation


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


class InvitationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Invitation
        fields = ['id', 'email', 'invited_by', 'company', 'role']

    def create(self, validated_data):
        invited_by = self.context.get('invited_by', None)
        company = self.context.get('company', None)
        _, activation_key = generate_sha1(
            validated_data.get('email'),
            settings.SECRET_KEY
        )
        invite = Invitation.objects.create(
            invited_by=invited_by,
            company=company,
            activation_key=activation_key,
            **validated_data
        )
        return invite
