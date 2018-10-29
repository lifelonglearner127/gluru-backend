from django.conf.urls import url

from profiles.views import (
    UserRetrieveUpdateAPIView, GetLoginUrlAPIView, LoginCallbackAPIView,
    RegistrationAPIView, CheckRegistrationAPIView
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^get-authorization-url/?$', GetLoginUrlAPIView.as_view()),
    url(r'^login-callback/?$', LoginCallbackAPIView.as_view()),
    url(r'^signup/?$', RegistrationAPIView.as_view()),
    url(r'^check-signup/?$', CheckRegistrationAPIView.as_view())
]
