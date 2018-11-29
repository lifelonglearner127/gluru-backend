from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from profiles.views import (
    CompanyViewSet, UserRetrieveUpdateAPIView, GetLoginUrlAPIView,
    LoginCallbackAPIView, GetSingupUrlAPIView, SignupAPIView,
    LogoutUrlAPIView
)

router = DefaultRouter()
router.register(r'company', CompanyViewSet, base_name='company')

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^get-authorization-url/?$', GetLoginUrlAPIView.as_view()),
    url(r'^login-callback/?$', LoginCallbackAPIView.as_view()),
    url(r'^get-signup-url/?$', GetSingupUrlAPIView.as_view()),
    url(r'^signup/?$', SignupAPIView.as_view()),
    url(r'^logout/?$', LogoutUrlAPIView.as_view()),
    url(r'^', include(router.urls)),
]
