from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from profiles import serializers as s


class GetLoginUrlAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            {
                'results': {
                    'login_url': 'ddd'
                }
            },
            status=status.HTTP_200_OK
        )


class LoginCallbackAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        user = authenticate(
            username='lifelonglearner127@outlook.com',
            password='gibupjo127'
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
                'results': {
                    'login_url': 'ddd'
                }
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
