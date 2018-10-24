from django.conf.urls import url

from profiles.views import (
    UserRetrieveUpdateAPIView
)

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view())
]
