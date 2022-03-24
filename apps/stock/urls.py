from rest_framework_nested import routers

from .views import *

router = routers.SimpleRouter()
router.register("brands", BrandViewSet)
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet)
router.register("order-items", OrderItemViewSet)

urlpatterns = router.urls
