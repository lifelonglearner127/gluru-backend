from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from profiles import views as v

router = DefaultRouter()
router.register(r'company', v.CompanyViewSet, base_name='company')
router.register(r'users', v.UserViewSet, base_name='user')
router.register(r'role', v.UserRoleViewSet, base_name='role')
router.register(r'permission', v.PermissionViewSet, base_name='permission')

urlpatterns = [
    url(r'^user/?$', v.UserRetrieveUpdateAPIView.as_view()),
    url(r'^get-authorization-url/?$', v.GetLoginUrlAPIView.as_view()),
    url(r'^login-callback/?$', v.LoginCallbackAPIView.as_view()),
    url(r'^get-signup-url/?$', v.GetSingupUrlAPIView.as_view()),
    url(r'^signup/?$', v.SignupAPIView.as_view()),
    url(r'^logout/?$', v.LogoutUrlAPIView.as_view()),
    url(r'^', include(router.urls)),
]
