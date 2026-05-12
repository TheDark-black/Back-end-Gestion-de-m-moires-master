from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemoireViewSet, MilestoneViewSet, DocumentViewSet, ObservationViewSet
router = DefaultRouter()
router.register('memoires', MemoireViewSet, basename='memoires')
router.register('milestones', MilestoneViewSet, basename='milestones')
router.register('documents', DocumentViewSet, basename='documents')
router.register('observations', ObservationViewSet, basename='observations')
urlpatterns = [path('', include(router.urls))]
