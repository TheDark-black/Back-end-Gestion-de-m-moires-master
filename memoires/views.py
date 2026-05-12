from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Memoire, Milestone, Document, Observation
from .serializers import MemoireSerializer, MilestoneSerializer, DocumentSerializer, ObservationSerializer
from common.permissions import IsEnseignant
class MemoireViewSet(viewsets.ModelViewSet):
    serializer_class = MemoireSerializer
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    def get_queryset(self):
        user = self.request.user
        if user.role == 'etudiant':
            return Memoire.objects.filter(student__user=user)
        elif user.role in ['enseignant', 'superviseur']:
            return Memoire.objects.filter(subject__encadrant__user=user)
        return Memoire.objects.all()
    @action(detail=True, methods=['post'], permission_classes=[IsEnseignant])
    def valider_soutenabilite(self, request, pk=None):
        memoire = self.get_object()
        memoire.soutenable = True
        memoire.date_validation_soutenabilite = timezone.now()
        memoire.save()
        return Response({'message': 'Memoire marque comme soutenable.'})
    @action(detail=True, methods=['post'], permission_classes=[IsEnseignant])
    def refuser_soutenabilite(self, request, pk=None):
        memoire = self.get_object()
        memoire.soutenable = False
        memoire.date_validation_soutenabilite = None
        memoire.save()
        return Response({'message': 'Soutenabilite refusee.'})
class MilestoneViewSet(viewsets.ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Milestone.objects.filter(memoire__id=self.request.query_params.get('memoire'))
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Document.objects.filter(memoire__id=self.request.query_params.get('memoire'))
class ObservationViewSet(viewsets.ModelViewSet):
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Observation.objects.filter(memoire__id=self.request.query_params.get('memoire'))
    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)
