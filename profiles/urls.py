from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from profiles import views as v

router = DefaultRouter()
router.register(r'company', v.CompanyViewSet, base_name='company')
router.register(r'users', v.UserViewSet, base_name='user')

urlpatterns = [
    url(
        r'^user/?$',
        v.GetUserAuthAPIView.as_view(),
        name='get_auth'
    ),
    url(
        r'^get-authorization-url/?$',
        v.GetLoginUrlAPIView.as_view(),
        name='get_login_url'
    ),
    url(
        r'^login-callback/?$',
        v.LoginCallbackAPIView.as_view(),
        name='login_callback'
    ),
    url(
        r'^get-signup-url/?$',
        v.GetSingupUrlAPIView.as_view(),
        name='get_signup_url'
    ),
    url(
        r'^signup/?$',
        v.SignupAPIView.as_view(),
        name='signup'
    ),
    url(
        r'^logout/?$',
        v.LogoutUrlAPIView.as_view(),
        name='logout'
    ),
    url(r'^', include(router.urls)),
]
