from rest_framework_nested import routers

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ProductViewSet,
)

router = routers.SimpleRouter()
router.register("brands", BrandViewSet, basename="brand")
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls
