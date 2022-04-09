from django.urls import include, path
from rest_framework_nested import routers

from apps.user.views import UserViewSet
from .views import *
from ..stock.views import BrandViewSet, CategoryViewSet, ProductViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register("company-types", CompanyTypeViewSet)
router.register("company-roles", RoleViewSet)
router.register("companies", CompanyViewSet)
router.register("company-details", CompanyDetailsViewSet)

companies_router = routers.NestedSimpleRouter(router, "companies", lookup="company")
companies_router.register(r"roles", CompanyRoleViewSet, basename="company-roles")
companies_router.register(r"users", UserViewSet, basename="company-users")

companies_router.register(r"brands", BrandViewSet, basename="company-brands")
companies_router.register(r"categories", CategoryViewSet, basename="company-categories")
companies_router.register(r"products", ProductViewSet, basename="company-products")
companies_router.register(r"orders", OrderViewSet, basename="company-orders")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(companies_router.urls)),
]
