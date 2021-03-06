import json
import requests
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    PermissionDenied, ValidationError, NotFound
)
from rest_framework.response import Response
from rest_framework.decorators import action
from gluru_backend.utils import generate_hash, get_ticket_creatable_companies
from profiles import models as m
from profiles import serializers as s
from profiles import permissions as p
from oxd import uma as api
from oxd import exceptions as e


class GetLoginUrlAPIView(APIView):
    permission_classes = (p.IsVisitor,)

    def get(self, request):
        url = api.get_authorization_url()
        return Response(
            {
                'results': {
                    'login_url': url
                }
            },
            status=status.HTTP_200_OK
        )


class LoginCallbackAPIView(APIView):
    permission_classes = (p.IsVisitor, )

    def get(self, request):
        token_json = api.get_token_from_callback(request.query_params)
        access_token = token_json.get('access_token')
        id_token = token_json.get('id_token')
        if not access_token or not id_token:
            raise e.OxdError('Invalid token')
        user = authenticate(
            request, access_token=access_token, id_token=id_token
        )

        if user is not None:
            user_serializer = s.UserSerializer(user)
            return Response(
                {
                    'results': user_serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'user': 'You are not registered on support portal yet'
            },
            status=status.HTTP_403_FORBIDDEN
        )


class GetSingupUrlAPIView(APIView):
    permission_classes = (p.IsVisitor,)

    def get(self, request):
        url = '{}/register?from=support'\
            .format(settings.GLUU_USER_APP_FRONTEND)
        return Response(
            {
                'results': {
                    'signup_url': url
                }
            },
            status=status.HTTP_200_OK
        )


class SignupAPIView(APIView):
    permission_classes = (p.IsVisitor,)

    def get(self, request):
        check_signup_endpoint = '{}/api/v1/confirm-created/'.format(
            settings.GLUU_USER_APP_BACKEND
        )

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'idp_uuid': request.query_params.get('idp_uuid', None),
            'email_hash': request.query_params.get('email_hash', None)
        }

        r = requests.post(
            check_signup_endpoint, data=json.dumps(data), headers=headers
        )

        if r.status_code == 200:
            response = r.json()
            user = response.get('user')
            invite = response.get('invite')

            email = user.get('email')
            idp_uuid = user.get('idpUuid')
            first_name = user.get('firstName')
            last_name = user.get('lastName')

            user = m.Invitation.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                idp_uuid=idp_uuid
            )

            company = invite.get('company')
            activation_key = invite.get('activationKey')

            if company is not None and activation_key is not None:
                try:
                    invite = m.Invitation.objects.get(
                        company__id=company,
                        activation_key=activation_key
                    )
                except m.Invitation.DoesNotExist:
                    pass

                if email != invite.email:
                    pass

                if user in invite.company.users.all():
                    pass

                invite.accept(user)

            user_serializer = s.UserSerializer(user)
            return Response(
                {
                    'results': user_serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            raise ValidationError('Incorrect activation key')


class LogoutUrlAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        url = api.get_logout_url(id_token=request.user.id_token)
        return Response(
            {
                'results': {
                    'logout_url': url
                }
            },
            status=status.HTTP_200_OK
        )


class GetUserAuthAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = s.UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        return m.User.objects.all()

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())

        serializer = s.UserSerializer(
            page,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        pass

    @action(detail=False, methods=['GET'])
    def me(self, request, *args, **kwargs):
        # Get User Personal Data from Account Management App
        fetch_profile_endpoint = '{}/api/v1/fetch-profile/'.format(
            settings.GLUU_USER_APP_BACKEND
        )

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'idp_uuid': request.user.idp_uuid,
            'email_hash': generate_hash(request.user.email)
        }

        r = requests.post(
            fetch_profile_endpoint, data=json.dumps(data), headers=headers
        )

        if r.status_code == 200:
            response = r.json()
            data = {
                "address": response.get('address'),
                "timezone": response.get('timezone'),
                "job_title": response.get('job_title'),
                "about": response.get('about'),
            }

        personal_profile_serializer = s.PersonalProfileSerializer(data)
        association_serializer = s.UserAssociationSerializer(request.user)

        return Response(
            {'results': {
                'profile': personal_profile_serializer.data,
                'associations': association_serializer.data
            }},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], url_path='edit-profile')
    def edit_profile(self, request, *args, **kwargs):
        update_profile_endpoint = '{}/user-profile/'.format(
            settings.GLUU_USER_APP_FRONTEND
        )
        return Response(
            {'results': update_profile_endpoint},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'])
    def staffs(self, request, *args, **kwargs):
        staffs = m.User.objects.filter(is_staff=True)
        serializer = s.ShortUserSerializer(staffs, many=True)
        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'])
    def companies(self, request, *args, **kwargs):
        companies = m.Membership.objects.filter(user=request.user)
        serializer = s.UserMembershipSerializer(companies, many=True)
        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )


class CompanyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):

    permission_classes = (p.CompanyCustomPermission, )
    serializer_class = s.ShortCompanySerializer

    def get_queryset(self):
        return m.Company.objects.all()

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
        queryset = self.get_queryset() if request.user.is_staff else\
            request.user.companies

        serializer = self.serializer_class(
            self.paginate_queryset(queryset),
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

    @action(detail=False, methods=['GET'], url_path='ticket-createable')
    def ticket_creatable_companies(self, request):
        queryset = self.get_queryset().filter(
            get_ticket_creatable_companies(request.user)
        )

        serializer = self.serializer_class(
            queryset,
            many=True
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['GET'], url_path='users')
    def users(self, request, pk=None):
        serializer_instance = self.get_object()

        serializer = s.CompanySerializer(
            serializer_instance,
        )

        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['POST'])
    def invite(self, request, pk=None):
        company = self.get_object()
        serializer_data = request.data.get('invitation', {})

        email = serializer_data.get('email', None)
        try:
            invitation = m.Invitation.objects.get(
                email=email, company=company
            )
            msg = '{} already invited {} as {} in {}'.format(
                invitation.invited_by.email, email, invitation.role.name,
                company.name
            )
            raise ValidationError(msg)
        except m.Invitation.DoesNotExist:
            pass

        serializer = s.InvitationSerializer(
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

    @action(detail=True, methods=['POST'], url_path='accept-invite')
    def accept_invite(self, request, *args, **kwargs):
        company = self.get_object()
        activation_key = request.data.get('activation_key')

        try:
            invite = m.Invitation.objects.get(
                company=company,
                email=request.user.email,
                activation_key=activation_key
            )
        except m.Invitation.DoesNotExist:
            raise ValidationError('Invalid invite')

        if invite.is_accepted:
            raise ValidationError('You already accepted invitation')

        invite.accept(request.user)

        return Response({
            'results': 'Invite accepted successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='revoke-invite')
    def revoke_invite(self, request, *args, **kwargs):
        company = self.get_object()
        invite_id = request.data.get('invite_id', None)

        if invite_id is None:
            raise ValidationError('Invite id is required')

        try:
            invite = m.Invitation.objects.get(
                id=invite_id, company=company
            )
            invite.delete()
        except m.Invitation.DoesNotExist:
            NotFound(detail='Such invitation does not exist')

        return Response({
            'results': 'Invite revoked successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='remove-member')
    def remove_member(self, request, *args, **kwargs):
        company = self.get_object()
        user_id = request.data.get('user_id', None)
        if user_id is None:
            raise ValidationError('Invite id is required')

        try:
            user_id = int(user_id)
        except ValueError:
            raise ValidationError('Invalid user id')

        try:
            membership = m.Membership.objects.get(
                company=company,
                user__id=user_id
            )

            if membership.role.name == 'admin':
                raise ValidationError('Deleting company admin is prohibited')

            membership.delete()
        except m.Membership.DoesNotExist:
            raise NotFound('Such user does not exist')

        return Response({
            'results': 'User removed successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='leave-company')
    def leave_company(self, request, *args, **kwargs):
        company = self.get_object()
        try:
            membership = m.Membership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role.name == 'admin':
                raise ValidationError(
                    'You are admin of this company. Prohibited Operation'
                )
            else:
                membership.delete()
        except m.Membership.DoesNotExist:
            raise PermissionDenied('You are not member of this company')

        return Response({
            'results': 'User removed successfully'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='change-role')
    def change_role(self, request, *args, **kwargs):
        company = self.get_object()
        serializer_data = request.data.get('change_role', {})
        user_id = serializer_data.pop('user_id', None)

        try:
            user_id = int(user_id)
        except ValueError:
            raise ValidationError('Invalid user id')

        try:
            serializer_instance = m.Membership.objects.get(
                company=company, user__id=user_id
            )
            if serializer_instance.role.name == 'admin':
                raise ValidationError(
                    'Changing company admin role is prohibited'
                )
        except m.Membership.DoesNotExist:
            raise ValidationError('This user is not member of the company')

        serializer = s.ChangeRoleSerializer(
            serializer_instance,
            data=serializer_data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'results': serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, ticket_slug=None, pk=None):
        obj = self.get_object()
        obj.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
