from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HighlighterMixin
from tickets.search_indexes import TicketIndex
from tickets import models as m
from profiles.models import UserRole
from profiles.serializers import ShortUserSerializer, ShortCompanySerializer


class TicketSearchSerializer(HighlighterMixin, HaystackSerializer):
    highlighter_html_tag = "strong"
    highlighter_field = "body"

    class Meta:
        index_classes = [TicketIndex]

        fields = [
            "text", "category", "status", "issue_type", "gluu_server", "os",
            "created_by", "assignee", "company", "autocomplete"
        ]
        ignore_fields = ["autocomplete"]
        field_aliases = {
            "q": "autocomplete"
        }


class TicketProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.TicketProduct
        fields = (
            'product', 'os', 'os_version'
        )
        extra_kwargs = {
            'product': {'required': True},
            'os': {'required': True},
            'os_version': {'required': True}
        }


class TicketSerializer(serializers.ModelSerializer):
    created_by = ShortUserSerializer(read_only=True)
    created_for = ShortUserSerializer(read_only=True)
    assignee = ShortUserSerializer(read_only=True)
    updated_by = ShortUserSerializer(read_only=True)
    voters = ShortUserSerializer(many=True, required=False)
    subscribers = ShortUserSerializer(many=True, required=False)
    company_association = ShortCompanySerializer(read_only=True)
    products = TicketProductSerializer(
        source='ticketproduct_set', many=True, required=False
    )

    class Meta:
        model = m.Ticket
        fields = [
            'id', 'title', 'body', 'created_by', 'created_for', 'updated_by',
            'assignee', 'category', 'status', 'issue_type', 'gluu_server',
            'os', 'os_version', 'response_no', 'products', 'voters',
            'subscribers', 'company_association'
        ]
        extra_kwargs = {
            'category': {'required': True},
            'issue_type': {'required': True},
            'gluu_server': {'required': True},
            'os': {'required': True}
        }

    def create(self, validated_data):
        created_by = self.context.get('created_by', None)
        created_for_id = self.context.get('created_for', None)
        company_id = self.context.get('company_association', None)
        products = validated_data.pop('ticketproduct_set', [])

        created_for = None
        company_association = None

        if company_id is not None:
            company_association = get_object_or_404(m.Company, pk=company_id)
            if not created_by.is_superuser and created_by.is_staff:
                staff_role = UserRole.objects.get(name='staff')
                if not staff_role.has_permission(
                    app_name='tickets',
                    model_name='Ticket',
                    action='create'
                ):
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )

            if not created_by.is_staff:
                membership = created_by.membership_set.filter(
                    company=company_association
                ).first()

                if membership is None or membership.role is None:
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )

                if not membership.role.has_permission(
                    app_name='tickets',
                    model_name='Ticket',
                    action='create'
                ):
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )

        if created_for_id is not None and company_association is not None:
            created_for = get_object_or_404(m.User, pk=created_for_id)
            if not company_association.is_member(created_for):
                raise serializers.ValidationError(
                    "User is not a member of this company"
                )

        ticket = m.Ticket.objects.create(
            created_by=created_by,
            company_association=company_association,
            created_for=created_for,
            **validated_data
        )

        for product in products:
            m.TicketProduct.objects.create(
                ticket=ticket,
                product=product['product'],
                os=product['os'],
                os_version=product['os_version']
            )

        return ticket

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        assignee_id = self.context.get('assignee_id', None)
        if assignee_id is not None:
            try:
                assignee = m.User.objects.get(pk=assignee_id)
                instance.assignee = assignee
            except m.User.DoesNotExist:
                raise serializers.ValidationError('Such user does not exist')

        instance.updated_by = self.context.get('updated_by', None)

        instance.save()
        return instance


class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.TicketHistory
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    created_by = ShortUserSerializer(read_only=True)

    class Meta:
        model = m.Answer
        fields = [
            'id', 'body', 'ticket', 'created_by'
        ]
        extra_kwargs = {
            'ticket': {'required': False},
        }

    def create(self, validated_data):
        ticket = self.context.get('ticket', None)
        created_by = self.context.get('created_by', None)

        if not created_by.is_superuser and created_by.is_staff:
            staff_role = UserRole.objects.get(name='staff')
            if not staff_role.has_permission(
                app_name='tickets',
                model_name='Answer',
                action='create'
            ):
                raise PermissionDenied(
                    'You do not have permission to perform this action.'
                )
        if not created_by.is_staff:
            if ticket.company_association is None:
                if created_by != ticket.created_by:
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )
            else:
                membership = created_by.membership_set.filter(
                    company=ticket.company_association
                ).first()

                if membership is None or membership.role is None:
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )

                if not membership.role.has_permission(
                    app_name='tickets',
                    model_name='Answer',
                    action='create'
                ):
                    raise PermissionDenied(
                        'You do not have permission to perform this action.'
                    )

        return m.Answer.objects.create(
            ticket=ticket,
            created_by=created_by,
            **validated_data
        )

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.updated_by = self.context.get('updated_by', None)

        instance.save()
        return instance


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Document
        fields = '__all__'
