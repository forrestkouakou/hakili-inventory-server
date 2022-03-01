from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("user-permissions", UserPermissionViewSet)

urlpatterns = router.urls
