from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, UserViewSet, TeacherViewSet, StudentViewSet
router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet, basename='users')
router.register('teachers', TeacherViewSet, basename='teachers')
router.register('students', StudentViewSet, basename='students')
urlpatterns = [path('', include(router.urls))]
