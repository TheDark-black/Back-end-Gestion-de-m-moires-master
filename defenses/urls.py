from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DefenseSessionViewSet, DefenseViewSet, JuryViewSet,
                    JuryMemberViewSet, DefenseObservationViewSet, GradeViewSet)
router = DefaultRouter()
router.register('defense-sessions', DefenseSessionViewSet)
router.register('defenses', DefenseViewSet)
router.register('juries', JuryViewSet)
router.register('jury-members', JuryMemberViewSet)
router.register('defense-observations', DefenseObservationViewSet)
router.register('grades', GradeViewSet)
urlpatterns = [path('', include(router.urls))]
