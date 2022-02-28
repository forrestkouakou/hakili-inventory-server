from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("user-roles", UserRoleViewSet)
router.register("groups", GroupViewSet)
router.register("permissions", PermissionViewSet)

urlpatterns = router.urls
