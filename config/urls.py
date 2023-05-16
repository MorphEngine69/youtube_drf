from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='YouTube API',
        default_version='v1',
        description='no desc',
    ),
    patterns=[
        path('api/', include('api.urls')),
    ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        'api/v1/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger_api',
    ),
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    path('admin/', admin.site.urls),
    path('', include('videos.urls', namespace='videos')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
