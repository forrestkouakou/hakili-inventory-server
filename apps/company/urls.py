from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register("company-types", CompanyTypeViewSet)
router.register("company-roles", CompanyRoleViewSet)
router.register("companies", CompanyViewSet)
router.register("company-details", CompanyDetailsViewSet)

urlpatterns = router.urls
