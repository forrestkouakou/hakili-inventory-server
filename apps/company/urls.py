from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register("companies", CompanyViewSet)
router.register("company-types", CompanyTypeViewSet)

urlpatterns = router.urls
