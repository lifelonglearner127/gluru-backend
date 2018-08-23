from django.conf.urls import include, url

from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'search', views.TicketSearchView, base_name="location-search")

tickets_router = routers.NestedSimpleRouter(
    router,
    r'tickets',
    lookup='ticket'
)
tickets_router.register(
    r'answers',
    views.AnswerViewSet,
    base_name='ticket-answers'
)
tickets_router.register(
    r'history',
    views.TicketHistoryViewSet,
    base_name='ticket-history'
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(tickets_router.urls)),
]
