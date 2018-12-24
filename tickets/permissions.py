from django.shortcuts import get_object_or_404
from rest_framework import permissions
from profiles.models import Company, UserRole
from tickets.models import Ticket


class TicketCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or\
            request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            return staff_role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name=view.action
            )

        if obj.company_association is None:
            return request.method in permissions.SAFE_METHODS or\
                request.user == obj.created_by

        membership = None
        if request.user.is_authenticated:
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
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            model_name = 'Ticket' if view.action == 'retrieve' else\
                'Answer'
            return staff_role.has_permission(
                app_name='tickets',
                model_name=model_name,
                permission_name=view.action
            )

        kwargs = request.parser_context.get('kwargs')
        ticket_pk = kwargs.get('ticket_pk', None)
        if ticket_pk is None:
            return False

        ticket = get_object_or_404(Ticket, is_deleted=False, pk=ticket_pk)

        if ticket.company_association:
            if request.user.is_authenticated:
                membership = request.user.membership_set.filter(
                    company=ticket.company_association
                ).first()

                model_name = 'Ticket' if view.action == 'retrieve' else\
                    'Answer'
                return membership and membership.role and\
                    membership.role.has_permission(
                        app_name='tickets',
                        model_name=model_name,
                        permission_name=view.action
                    )
            else:
                return False
        else:
            if view.action == 'create':
                return request.user == ticket.created_by

            return request.method in permissions.SAFE_METHODS or\
                request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.ticket.company_association:
            if request.user.is_superuser:
                return True

            if request.user.is_staff:
                staff_role = UserRole.objects.get(name='staff')
                model_name = 'Ticket' if view.action == 'retrieve' else\
                    'Answer'
                return staff_role.has_permission(
                    app_name='tickets',
                    model_name=model_name,
                    permission_name=view.action
                )
            membership = request.user.membership_set.filter(
                company=obj.ticket.company_association
            ).first()

            model_name = 'Ticket' if view.action == 'retrieve' else 'Answer'
            return membership and membership.role and\
                membership.role.has_permission(
                    app_name='tickets',
                    model_name=model_name,
                    permission_name=view.action
                )
        else:
            return obj.created_by == request.user
