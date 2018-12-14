from rest_framework import permissions
from profiles.models import Company, UserRole


class TicketCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        else:
            if not request.user.is_authenticated:
                return False

            if request.user.is_superuser:
                return True

            if request.user.is_staff:
                staff_role = UserRole.objects.get(name='staff')
                return staff_role.has_permission(
                    app_name='tickets',
                    model_name='Ticket',
                    permission_name=view.action
                )

            if view.action == 'create':
                ticket_data = request.data.get('ticket', {})
                company_association = ticket_data.get(
                    'company_association', None
                )
                if company_association is not None:
                    try:
                        company = Company.objects.get(pk=company_association)
                        membership = request.user.membership_set.filter(
                            company=company
                        ).first()
                        return membership and membership.role and\
                            membership.role.has_permission(
                                app_name='tickets',
                                model_name='Ticket',
                                permission_name=view.action
                            )
                    except Company.DoesNotExist:
                        pass

            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.company_association is None:
            if request.method in ['GET']:
                return True
            if request.method in ['PUT']:
                return request.user == obj.created_by

        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            return staff_role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name=view.action
            )

        membership = request.user.membership_set.filter(
            company=obj.company_association
        ).first()

        return membership and membership.role and\
            membership.role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name=view.action
            )
