from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from tickets.serializers import TicketSerializer
from info.models import (
    GluuServer, GluuOS, GluuProduct, TicketIssueType, TicketCategory
)
from info.serializers import (
    GluuServerSerializer, GluuOSSerializer, GluuProductSerializer,
    TicketCategorySerializer, TicketIssueTypeSerializer
)


class GluuServerViewset(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = GluuServerSerializer

    def get_queryset(self):
        return GluuServer.objects.all()

    def create(self, request):
        serializer_data = request.data.get('server', {})
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
        serializer_data = self.get_queryset()

        serializer = self.serializer_class(
            serializer_data,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'])
    def tickets(self, request, pk=None):
        server = self.get_object()
        page = self.paginate_queryset(server.tickets.all())

        serializer = TicketSerializer(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('server', {})
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

    def destroy(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GluuOSViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = GluuOSSerializer

    def get_queryset(self):
        return GluuOS.objects.all()

    def create(self, request):
        serializer_data = request.data.get('os', {})
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
        serializer_data = self.get_queryset()

        serializer = self.serializer_class(
            serializer_data,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'])
    def tickets(self, request, pk=None):
        os = self.get_object()
        page = self.paginate_queryset(os.tickets.all())

        serializer = TicketSerializer(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('os', {})
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

    def destroy(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GluuProductViewset(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = GluuProductSerializer

    def get_queryset(self):
        return GluuProduct.objects.all()

    def create(self, request):
        serializer_data = request.data.get('product', {})
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
        serializer_data = self.get_queryset()

        serializer = self.serializer_class(
            serializer_data,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('product', {})
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

    def destroy(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TicketCategoryViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = TicketCategorySerializer

    def get_queryset(self):
        return TicketCategory.objects.all()

    def create(self, request):
        serializer_data = request.data.get('ticket_category', {})
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
        serializer_data = self.get_queryset()

        serializer = self.serializer_class(
            serializer_data,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'])
    def tickets(self, request, pk=None):
        category = self.get_object()
        page = self.paginate_queryset(category.tickets.all())

        serializer = TicketSerializer(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('ticket_category', {})
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

    def destroy(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TicketIssueTypeViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = ()
    serializer_class = TicketIssueTypeSerializer

    def get_queryset(self):
        return TicketIssueType.objects.all()

    def create(self, request):
        serializer_data = request.data.get('ticket_issue_type', {})
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
        serializer_data = self.get_queryset()

        serializer = self.serializer_class(
            serializer_data,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'])
    def tickets(self, request, pk=None):
        issue_type = self.get_object()
        page = self.paginate_queryset(issue_type.tickets.all())

        serializer = TicketSerializer(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, pk=None):
        serializer_instance = self.get_object()
        serializer_data = request.data.get('ticket_issue_type', {})
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

    def destroy(self, request, pk=None):
        obj = self.get_object()
        obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
