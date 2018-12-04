from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from info.views import (
    GluuServerViewset, GluuOSViewSet, GluuProductViewset,
    TicketCategoryViewSet, TicketIssueTypeViewSet, GetAllInfoView
)

router = DefaultRouter()
router.register(r'server', GluuServerViewset, base_name='server')
router.register(r'os', GluuOSViewSet, base_name='os')
router.register(r'product', GluuProductViewset, base_name='product')
router.register(r'category', TicketCategoryViewSet, base_name="category")
router.register(r'issue-type', TicketIssueTypeViewSet, base_name="issue-type")

urlpatterns = [
    url(r'^all/?$', GetAllInfoView.as_view()),
    url(r'^', include(router.urls)),
]
