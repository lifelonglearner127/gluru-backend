from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from info import views as v

router = DefaultRouter()
router.register(r'server', v.GluuServerViewset, base_name='server')
router.register(r'os', v.GluuOSViewSet, base_name='os')
router.register(r'product', v.GluuProductViewset, base_name='product')
router.register(r'category', v.TicketCategoryViewSet, base_name="category")
router.register(r'issue-type', v.TicketIssueTypeViewSet, base_name="type")
router.register(r'status', v.TicketStatusViewSet, base_name="status")

urlpatterns = [
    url(r'^all/?$', v.GetAllInfoView.as_view()),
    url(r'^', include(router.urls)),
]
