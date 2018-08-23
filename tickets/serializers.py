from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HighlighterMixin
from tickets.search_indexes import TicketIndex
from tickets.models import (
    Ticket, Answer, TicketHistory
)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketSearchSerializer(HighlighterMixin, HaystackSerializer):
    highlighter_html_tag = "strong"
    highlighter_field = "status"
    class Meta:
        index_classes = [TicketIndex]

        fields = [
            "text", "status", "os_version", "server_version", "category",
            "is_private", "created_by", "created_for", "company", "created_at"
        ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = (
            'id',
            'body',
            'created_by',
            'privacy'
        )

    def create(self, valdiated_data):
        ticket = self.context['ticket']
        return Answer.objects.create(
            ticket=ticket,
            **valdiated_data
        )


class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketHistory
        fields = (
            'changed_by',
            'changed_field',
            'before_value',
            'after_value',
            'created_at'
        )