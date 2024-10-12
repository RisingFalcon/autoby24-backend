from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AutoBy24 API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

admin.site.site_title = "AutoBy24"
admin.site.site_header = "AutoBy24"
admin.site.index_title = "Site administration"

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
	schema_view.without_ui(cache_timeout=0), name='schema-json'),
	re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-	swagger-ui'), # doc url
	# re_path(r'^redoc/$', schema_view.with_ui('redoc',
	# cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)