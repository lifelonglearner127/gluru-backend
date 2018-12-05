from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.serializers import HighlighterMixin
from tickets.search_indexes import TicketIndex
from tickets import models as m
from profiles.serializers import ShortUserSerializer


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
    updated_by = ShortUserSerializer(read_only=True)
    products = TicketProductSerializer(
        source='ticketproduct_set', many=True, required=False
    )

    class Meta:
        model = m.Ticket
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

        ticket = m.Ticket.objects.create(
            created_by=created_by,
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


class TicketVoteSerializer(serializers.ModelSerializer):

    voter = ShortUserSerializer(read_only=True)

    class Meta:
        model = m.TicketVote
        fields = [
            'voter', 'ticket', 'is_up'
        ]
        extra_kwargs = {
            'ticket': {'required': False},
        }
    
    def create(self, validated_data):
        ticket = self.context.get('ticket', None)
        voter = self.context.get('voter', None)
        return m.TicketVote.objects.create(
            ticket=ticket,
            voter=voter,
            **validated_data
        )


class VoterTicketVoteSerializer(serializers.ModelSerializer):

    voter = ShortUserSerializer(read_only=True)

    class Meta:
        model = m.TicketVote
        fields = (
            'voter', 'is_up'
        )


class TicketVoterSerializer(serializers.ModelSerializer):
    
    voters = VoterTicketVoteSerializer(
        source='ticketvote_set', many=True, required=False
    )

    class Meta:
        model = m.Ticket
        fields = [
            'voters'
        ]
