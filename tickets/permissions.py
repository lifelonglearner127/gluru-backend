from django.shortcuts import get_object_or_404
from rest_framework import permissions
from profiles.models import UserRole
from tickets.models import Ticket


class TicketCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or\
            request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        permission_name = 'retrieve'\
            if request.method in permissions.SAFE_METHODS else view.action

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            return staff_role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name=permission_name
            )

        company = obj.company_association
        if company is None:
            return request.method in permissions.SAFE_METHODS or\
                request.user == obj.created_by

        if not request.user.is_authenticated:
            return False

        membership = company.membership_set.filter(user=request.user).first()

        return membership and membership.role and\
            membership.role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name=permission_name
            )


class AnswerCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or\
            request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            model_name = 'Ticket' if view.action == 'retrieve' else 'Answer'
            return staff_role.has_permission(
                app_name='tickets',
                model_name=model_name,
                permission_name=view.action
            )
            membership = request.user.membership_set.filter(
                company=obj.ticket.company_association
            ).first()

        if obj.ticket.company_association is None:
            return request.method in permissions.SAFE_METHODS or\
                request.user == obj.created_by

        membership = None
        if request.user.is_authenticated:
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


class TicketAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        kwargs = request.parser_context.get('kwargs')
        ticket_pk = kwargs.get('ticket_pk', None)
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        company = ticket.company_association

        if company is None:
            return True

        if request.user.is_superuser:
            return True

        if request.user.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            return staff_role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name='retrieve'
            )

        membership = company.membership_set.filter(user=request.user).first()
        return membership and membership.role and\
            membership.role.has_permission(
                app_name='tickets',
                model_name='Ticket',
                permission_name='retrieve'
            )
