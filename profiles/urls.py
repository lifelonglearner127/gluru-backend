from django.conf.urls import url

from profiles.views import (
    UserRetrieveUpdateAPIView, GetLoginUrlAPIView, LoginCallbackAPIView
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^get-authorization-url/?$', GetLoginUrlAPIView.as_view()),
    url(r'^login-callback/?$', LoginCallbackAPIView.as_view())
]
