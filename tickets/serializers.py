from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HighlighterMixin
from profiles.serializers import ShortUserSerializer
from tickets.search_indexes import TicketIndex
from tickets.models import (
    Ticket, TicketProduct, TicketHistory, Answer
)


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
        model = TicketProduct
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
    updated_by = ShortUserSerializer(read_only=True)
    products = TicketProductSerializer(
        source='ticketproduct_set', many=True, required=False
    )

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'body', 'created_by', 'created_for', 'updated_by',
            'assignee', 'category', 'status', 'issue_type', 'gluu_server',
            'os', 'os_version', 'response_no', 'products'
        ]
        extra_kwargs = {
            'category': {'required': True},
            'issue_type': {'required': True},
            'gluu_server': {'required': True},
            'os': {'required': True}
        }

    def create(self, validated_data):
        created_by = self.context.get('created_by', None)
        products = validated_data.pop('ticketproduct_set', [])

        ticket = Ticket.objects.create(
            created_by=created_by,
            **validated_data
        )

        for product in products:
            TicketProduct.objects.create(
                ticket=ticket,
                product=product['product'],
                os=product['os'],
                os_version=product['os_version']
            )

        return ticket

    def update(self, instance, validated_data):
        instance.title = validated_data.get(
            'title', instance.title
        )
        instance.body = validated_data.get(
            'body', instance.body
        )
        instance.assignee = validated_data.get(
            'assignee', instance.assignee
        )
        instance.category = validated_data.get(
            'category', instance.category
        )
        instance.status = validated_data.get(
            'status', instance.status
        )
        instance.issue_type = validated_data.get(
            'issue_type', instance.issue_type
        )
        instance.gluu_server = validated_data.get(
            'gluu_server', instance.gluu_server
        )
        instance.os = validated_data.get(
            'os', instance.os
        )
        instance.updated_by = self.context.get('updated_by', None)

        instance.save()
        return instance


class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketHistory
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    created_by = ShortUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = [
            'id', 'body', 'ticket', 'created_by'
        ]
        extra_kwargs = {
            'ticket': {'required': False},
        }

    def create(self, validated_data):
        ticket = self.context.get('ticket', None)
        created_by = self.context.get('created_by', None)
        answer = Answer.objects.create(
            ticket=ticket,
            created_by=created_by,
            **validated_data
        )
        return answer

    def update(self, instance, validated_data):
        instance.body = validated_data.get(
            'body', instance.body
        )
        instance.updated_by = self.context.get('updated_by', None)

        instance.save()
        return instance
