from django.conf.urls import url, include
from profiles.views import UserRetrieveUpdateAPIView
from rest_framework.routers import DefaultRouter
from profiles.views import CompanyViewSet

router = DefaultRouter()
router.register(r'company', CompanyViewSet, base_name='company')

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^', include(router.urls)),
]
