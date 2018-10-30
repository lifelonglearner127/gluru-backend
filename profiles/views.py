import json
import requests
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from profiles import serializers as s
from profiles import models as m
from oxd import uma as api
from oxd import exceptions as e
from django.conf import settings


class GetLoginUrlAPIView(APIView):
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny, )

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
    permission_classes = (AllowAny,)

    def get(self, request):
        url = '{}/register?from=support'\
            .format(settings.GLUU_USER_FRONTEND_APP)
        return Response(
            {
                'results': {
                    'signup_url': url
                }
            },
            status=status.HTTP_200_OK
        )


class CheckRegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = s.UserSerializer

    def post(self, request):
        email = request.data.get('email', None)
        unique_key = request.data.get('unique_key', None)
        if email is None or unique_key is None:
            return Response(
                {
                    'results': {
                        'error': 'Email Or Unique Key is missing'
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = settings.GLUU_USER_BACKEND_APP + '/api/v1/confirm-created/'
        data = {
            'email': email,
            'uniqueKey': unique_key
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            return Response(
                {
                    'results': {
                        'error': 'Not created on Gluu users yet'
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = r.json()
        user_details = response.get('results')
        user_data = {
            'idp_uuid': user_details.get('idpUuid'),
            'first_name': user_details.get('firstName'),
            'last_name': user_details.get('lastName'),
            'email': user_details.get('email'),
        }
        user = m.User.objects.create(**user_data)
        serializer = self.serializer_class(user)
        return Response(
            {
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = s.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(
            {
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        print(user_data)
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
            {
                'results': serializer.data
            },
            status=status.HTTP_200_OK
        )
