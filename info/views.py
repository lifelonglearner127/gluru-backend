from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from tickets.serializers import TicketSerializer
from info import models as m
from info import serializers as s
from info import permissions as p


class GetAllInfoView(APIView):
    def get(self, reqeust):
        servers = m.GluuServer.objects.all()
        products = m.GluuProduct.objects.all()
        os = m.GluuOS.objects.all()
        issue_types = m.TicketIssueType.objects.all()
        categories = m.TicketCategory.objects.all()

        server_serializer = s.GluuServerSerializer(
            servers,
            many=True
        )
        product_serializer = s.GluuProductSerializer(
            products,
            many=True
        )
        os_serializer = s.GluuOSSerializer(
            os,
            many=True
        )
        type_serializer = s.TicketIssueTypeSerializer(
            issue_types,
            many=True
        )
        category_serializer = s.TicketCategorySerializer(
            categories,
            many=True
        )
        return Response({
                'servers': server_serializer.data,
                'products': product_serializer.data,
                'os': os_serializer.data,
                'types': type_serializer.data,
                'categories': category_serializer.data
            },
            status=status.HTTP_200_OK
        )


class GluuServerViewset(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = s.GluuServerSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.GluuServer.objects.all()

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
    serializer_class = s.GluuOSSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.GluuOS.objects.all()

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
    serializer_class = s.GluuProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.GluuProduct.objects.all()

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
    serializer_class = s.TicketCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.TicketCategory.objects.all()

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
    serializer_class = s.TicketIssueTypeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.TicketIssueType.objects.all()

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


class TicketStatusViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = s.TicketStatusSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.TicketStatus.objects.all()

    def create(self, request):
        serializer_data = request.data.get('ticket_status', {})
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
        serializer_data = request.data.get('ticket_status', {})
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


class UserRoleViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = s.UserRoleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.UserRole.objects.all()

    def create(self, request):
        serializer_data = request.data.get('role', {})
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
        serializer_data = request.data.get('role', {})
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


class PermissionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = s.PermissionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [p.IsSuperUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return m.Permission.objects.all()

    def create(self, request):
        serializer_data = request.data.get('permission', {})
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
        serializer_data = request.data.get('permission', {})
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
