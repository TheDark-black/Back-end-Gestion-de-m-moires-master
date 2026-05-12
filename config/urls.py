from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Refresh token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentation Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Apps
    path('api/', include('accounts.urls')),
    path('api/', include('academics.urls')),
    path('api/', include('subjects.urls')),
    path('api/', include('applications.urls')),
    path('api/', include('memoires.urls')),
    path('api/', include('defenses.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)