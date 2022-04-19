from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="user")
router.register("installations", InstallationViewSet, basename="installation")

urlpatterns = router.urls
