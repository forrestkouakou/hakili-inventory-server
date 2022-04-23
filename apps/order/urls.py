from rest_framework_nested import routers

from .views import (
    OrderViewSet,
    OrderItemViewSet,
)

router = routers.SimpleRouter()
router.register("orders", OrderViewSet, basename="order")
router.register("order-items", OrderItemViewSet)

urlpatterns = router.urls
