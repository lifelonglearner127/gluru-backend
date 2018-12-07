from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackAutocompleteFilter
from tickets import models as m
from tickets import serializers as s


class TicketSearchView(HaystackViewSet):
    index_models = [m.Ticket]
    serializer_class = s.TicketSearchSerializer
    filter_backends = [HaystackAutocompleteFilter]


class TicketViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = s.TicketSerializer

    def get_queryset(self):
        return m.Ticket.actives.all()

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

    @action(detail=True, methods=['POST'])
    def vote(self, request, pk=None):
        ticket = self.get_object()
        serializer_data = request.data.get('vote', {})
        context = {
            'ticket': ticket,
            'voter': request.user
        }
        serializer = s.TicketVoteSerializer(
            data=serializer_data, context=context
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['GET'])
    def voters(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer = s.TicketVoterSerializer(
            serializer_instance,
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser])
    def upload(self, request, pk=None):
        obj = self.get_object()
        files = list(request.FILES.values())
        for f in files:
            serializer = s.DocumentSerializer(data={"file": f})
            serializer.is_valid(raise_exception=True)
            document = serializer.save()
            m.Attachments.objects.create(
                document=document,
                ticket=obj
            )

        return Response(
            {'results': 'Successfully uploaded'},
            status=status.HTTP_200_OK
        )


class AnswerViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = s.AnswerSerializer

    def get_queryset(self):
        return m.Answer.actives.filter(
            ticket=self.kwargs['ticket_pk'],
            ticket__is_deleted=False
        )

    def create(self, request, ticket_pk=None):
        serializer_data = request.data.get('answer', {})
        ticket = get_object_or_404(m.Ticket, is_deleted=False, pk=ticket_pk)
        context = {
            'created_by': request.user,
            'ticket': ticket
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

    @action(detail=True, methods=['PUT'], parser_classes=[MultiPartParser])
    def upload(self, request, ticket_pk=None, pk=None):
        obj = self.get_object()
        files = list(request.FILES.values())
        for f in files:
            serializer = s.DocumentSerializer(data={"file": f})
            serializer.is_valid(raise_exception=True)
            document = serializer.save()
            m.Attachments.objects.create(
                document=document,
                answer=obj
            )

        return Response(
            {'results': 'Successfully uploaded'},
            status=status.HTTP_200_OK
        )


class TicketHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = s.TicketHistorySerializer

    def get_queryset(self):
        return m.TicketHistory.objects.filter(
            ticket=self.kwargs['ticket_pk'],
            ticket__is_deleted=False
        )
