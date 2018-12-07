from django.conf import settings
from rest_framework import serializers
from gluru_backend.utils import generate_sha1
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


class InvitationSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = m.Invitation
        fields = ['id', 'email', 'invited_by', 'company', 'role']

    def create(self, validated_data):
        invited_by = self.context.get('invited_by', None)
        company = self.context.get('company', None)
        _, activation_key = generate_sha1(
            validated_data.get('email'),
            settings.SECRET_KEY
        )
        return m.Invitation.objects.create(
            invited_by=invited_by,
            company=company,
            activation_key=activation_key,
            **validated_data
        )


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Permission
        fields = '__all__'


class UserRolePermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.UserRolePermission
        fields = [
            'permission', 'is_enabled'
        ]


class UserRoleSerializer(serializers.ModelSerializer):

    permissions = UserRolePermissionSerializer(
        source='userrolepermission_set', many=True, required=False
    )

    class Meta:
        model = m.UserRole
        fields = [
            'name', 'permissions'
        ]

    def create(self, validated_data):
        permissions = self.context.get('permissions', [])
        role = m.UserRole.objects.create(
            **validated_data
        )
        for p in permissions:
            try:
                permission_id = int(p['id'])
            except ValueError:
                continue

            try:
                permission = m.Permission.objects.get(pk=permission_id)
            except m.Permission.DoesNotExist:
                continue

            role_permission, _ = m.UserRolePermission.objects.get_or_create(
                role=role,
                permission=permission
            )
            role_permission.is_enabled = p['is_enabled']
            role_permission.save()

        return role

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        permissions = self.context.get('permissions', [])

        for p in permissions:
            try:
                permission_id = int(p['id'])
            except ValueError:
                continue

            try:
                permission = m.Permission.objects.get(pk=permission_id)
            except m.Permission.DoesNotExist:
                continue

            role_permission, _ = m.UserRolePermission.objects.get_or_create(
                role=instance,
                permission=permission
            )
            role_permission.is_enabled = p['is_enabled']
            role_permission.save()

        instance.save()
        return instance
