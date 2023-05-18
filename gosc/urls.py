"""gosc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

from . import views
from . import admin_site
from . import check


check.check_setting()


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="一体化云服务 API",
        default_version='v1',
    ),
    url=getattr(settings, 'SWAGGER_SCHEMA_URL', None),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls', namespace='users')),
    path('servers/', include('servers.urls', namespace='servers')),
    path('service/', include('service.urls', namespace='service')),
    path('api/', include('api.urls', namespace='api')),
    path('vpn/', include('vpn.urls', namespace='vpn')),
    path('apidocs/', schema_view.with_ui('swagger', cache_timeout=0), name='apidocs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('docs/', include('docs.urls', namespace='docs')),
    path('about/', views.about, name='about'),
    path('report/', include('report.urls', namespace='report')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
