from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DefenseSession, Defense, Jury, JuryMember, DefenseObservation, Grade
from .serializers import (DefenseSessionSerializer, DefenseSerializer, JurySerializer,
                           JuryMemberSerializer, DefenseObservationSerializer, GradeSerializer)
from common.permissions import IsResponsable
class DefenseSessionViewSet(viewsets.ModelViewSet):
    queryset = DefenseSession.objects.all()
    serializer_class = DefenseSessionSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [IsAuthenticated()]
class DefenseViewSet(viewsets.ModelViewSet):
    queryset = Defense.objects.all()
    serializer_class = DefenseSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [IsAuthenticated()]
    @action(detail=True, methods=['post'], permission_classes=[IsResponsable])
    def marquer_tenue(self, request, pk=None):
        defense = self.get_object()
        defense.tenue_effective = True
        defense.statut = 'tenue'
        defense.save()
        return Response({'message': 'Soutenance marquee comme tenue.'})
class JuryViewSet(viewsets.ModelViewSet):
    queryset = Jury.objects.all()
    serializer_class = JurySerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [IsAuthenticated()]
class JuryMemberViewSet(viewsets.ModelViewSet):
    queryset = JuryMember.objects.all()
    serializer_class = JuryMemberSerializer
    permission_classes = [IsResponsable]
class DefenseObservationViewSet(viewsets.ModelViewSet):
    queryset = DefenseObservation.objects.all()
    serializer_class = DefenseObservationSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)
class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsResponsable]
