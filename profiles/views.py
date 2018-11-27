from rest_framework import viewsets, mixins, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from profiles.models import Company
from profiles.serializers import (
    UserSerializer, CompanySerializer, ShortCompanySerializer,
    InvitationSerializer
)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        serializer_data = {
            'first_name': user_data.get('first_name', request.user.first_name),
            'last_name': user_data.get('last_name', request.user.last_name),
            'email': user_data.get('email', request.user.email)
        }

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )


class CompanyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):

    serializer_class = ShortCompanySerializer

    def get_queryset(self):
        return Company.objects.all()

    def create(self, request):
        serializer_data = request.data.get('company', {})
        serializer = self.serializer_class(
            data=serializer_data
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
        serializer_data = request.data.get('company', {})
        serializer = self.serializer_class(
            serializer_instance,
            data=serializer_data,
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

    @action(
        detail=True, methods=['GET'], url_path='users'
    )
    def users(self, request, pk=None):
        serializer_instance = self.get_object()

        serializer = CompanySerializer(
            serializer_instance,
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(
        detail=True, methods=['POST']
    )
    def invite(self, request, pk=None):
        company = self.get_object()
        serializer_data = request.data.get('invitation', {})

        serializer = InvitationSerializer(
            data=serializer_data,
            context={
                'invited_by': request.user,
                'company': company
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'results': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, ticket_pk=None, pk=None):
        obj = self.get_object()
        obj.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
