from rest_framework import permissions


class TicketCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET'] or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.company_association is None:
            return True

        membership = request.user.membership_set.filter(
            company=obj.company_association
        ).first()

        return membership and membership.role and\
            membership.role.has_permission(view.action)
