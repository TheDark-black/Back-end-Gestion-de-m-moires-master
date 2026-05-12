from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, UserViewSet, TeacherViewSet, StudentViewSet,
    PasswordResetRequestView, PasswordResetConfirmView
)

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('teachers', TeacherViewSet, basename='teachers')
router.register('students', StudentViewSet, basename='students')

urlpatterns = [
    # Routes du router (ViewSets)
    path('', include(router.urls)),

    # Routes manuelles (reset password)
    path('auth/reset-password/', PasswordResetRequestView.as_view(), name='reset-password'),
    path('auth/reset-password/confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]