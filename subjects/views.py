from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer
from common.permissions import IsEnseignant
class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'mots_cles']
    ordering_fields = ['titre', 'statut']
    def get_queryset(self):
        user = self.request.user
        qs = Subject.objects.select_related('encadrant', 'superviseur', 'semester')
        if user.role == 'etudiant':
            return qs.filter(statut='publie')
        return qs
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsEnseignant()]
        return [IsAuthenticated()]
