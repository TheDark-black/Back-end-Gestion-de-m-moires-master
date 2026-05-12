from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcademicYearViewSet, SemesterViewSet
router = DefaultRouter()
router.register('academic-years', AcademicYearViewSet)
router.register('semesters', SemesterViewSet)
urlpatterns = [path('', include(router.urls))]
