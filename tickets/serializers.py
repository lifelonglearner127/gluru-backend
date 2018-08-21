from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HighlighterMixin
from tickets.models import Ticket, Answer
from tickets.search_indexes import TicketIndex


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketSearchSerializer(HighlighterMixin, HaystackSerializer):
    highlighter_css_class = "my-highlighter-class"
    highlighter_html_tag = "em"

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
