from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('accounts.urls')),
    path('api/', include('academics.urls')),
    path('api/', include('subjects.urls')),
    path('api/', include('applications.urls')),
    path('api/', include('memoires.urls')),
    path('api/', include('defenses.urls')),
]
