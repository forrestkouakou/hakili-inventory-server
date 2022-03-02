from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.utils.translation import gettext_lazy
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from apps.core import views

admin.site.site_title = gettext_lazy('Administration HAKILI')
admin.site.site_header = gettext_lazy('Administration HAKILI')

schema_view = get_schema_view(
    openapi.Info(
        title="HAKILI API",
        default_version='v1',
        description="HAKILI SERVER",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # re_path(r'^api/(?P<version>(v1|v2))/', include('apps.user.urls'), name="api"),
    re_path(r'^api/(?P<version>(v1|v2))/', include('apps.company.urls'), name="api"),

    re_path(r'^api/(?P<version>(v1|v2))/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/(?P<version>(v1|v2))/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('alive', views.is_alive, name="is_alive"),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('admin/', admin.site.urls),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    path('hakili/accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
