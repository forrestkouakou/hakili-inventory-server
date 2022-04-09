from rest_framework_nested import routers

from .views import *

router = routers.SimpleRouter()
router.register("brands", BrandViewSet, basename="brand")
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")
router.register("order-items", OrderItemViewSet)

urlpatterns = router.urls
