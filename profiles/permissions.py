from rest_framework import permissions


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
        return True
