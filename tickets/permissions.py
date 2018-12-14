from django.shortcuts import get_object_or_404
from rest_framework import permissions
from profiles.models import Company, UserRole
from tickets.models import Ticket


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
            if request.method in ['PUT', 'DELETE']:
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


class AnswerCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        kwargs = request.parser_context.get('kwargs')
        ticket_pk = kwargs.get('ticket_pk', None)
        if ticket_pk is None:
            return False

        ticket = get_object_or_404(Ticket, is_deleted=False, pk=ticket_pk)

        staff_role = UserRole.objects.get(name='staff')

        if ticket.company_association is None:
            if request.user.is_superuser:
                return True

            if request.user.is_staff:
                model_name = 'Ticket' if view.action == 'retrieve' else\
                    'Answer'
                return staff_role.has_permission(
                    app_name='tickets',
                    model_name=model_name,
                    permission_name=view.action
                )

            return ticket.created_by == request.user
        else:
            if not request.user.is_authenticated:
                return False
            membership = request.user.membership_set.filter(
                company=ticket.company_association
            ).first()

            model_name = 'Ticket' if view.action == 'retrieve' else 'Answer'
            return membership and membership.role and\
                membership.role.has_permission(
                    app_name='tickets',
                    model_name=model_name,
                    permission_name=view.action
                )

    def has_object_permission(self, request, view, obj):
        return True
