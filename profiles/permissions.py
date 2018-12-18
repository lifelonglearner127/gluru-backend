from rest_framework import permissions
from info.models import UserRole


class IsCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.company == obj


class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj in request.user.companies


class IsStaffOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.id == request.user.id


class CompanyCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'update']:
            return request.user.is_authenticated and request.user.is_superuser

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET'] or view.action in ['accept_invite']:
            return request.user.is_authenticated

        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            return staff_role.has_permission(
                app_name='profiles',
                model_name='Company',
                permission_name=view.action
            )

        membership = request.user.membership_set.filter(
            company=obj
        ).first()

        return membership and membership.role and\
            membership.role.has_permission(
                app_name='profiles',
                model_name='Company',
                permission_name=view.action
            )
