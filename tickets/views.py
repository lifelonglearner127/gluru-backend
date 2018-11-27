from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackAutocompleteFilter
from tickets.models import (
    Ticket,  Answer, TicketHistory
)
from tickets.serializers import (
    TicketSerializer, AnswerSerializer, TicketSearchSerializer,
    TicketHistorySerializer
)


class TicketSearchView(HaystackViewSet):
    index_models = [Ticket]
    serializer_class = TicketSearchSerializer
    filter_backends = [HaystackAutocompleteFilter]


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.actives.all()

    def create(self, request):
        serializer_data = request.data.get('ticket', {})
        context = {
            'created_by': request.user
        }
        serializer = self.serializer_class(
            data=serializer_data, context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('ticket', {})
        context = {
            'updated_by': request.user
        }
        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer = self.serializer_class(
            serializer_instance,
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        ticket = self.get_object()
        ticket.is_deleted = True
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.actives.filter(
            ticket=self.kwargs['ticket_pk'],
            ticket__is_deleted=False
        )

    def create(self, request, ticket_pk=None):
        serializer_data = request.data.get('answer', {})
        context = {
            'created_by': request.user,
            'ticket': get_object_or_404(Ticket, is_deleted=False, pk=ticket_pk)
        }
        serializer = self.serializer_class(
            data=serializer_data,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, ticket_pk=None, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('answer', {})
        context = {
            'updated_by': request.user
        }
        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, ticket_pk=None, pk=None):
        answer = self.get_object()
        answer.is_deleted = True
        answer.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TicketHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = TicketHistorySerializer

    def get_queryset(self):
        return TicketHistory.objects.filter(
            ticket=self.kwargs['ticket_pk'],
            ticket__is_deleted=False
        )
