from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from common.permissions import IsEnseignant, IsEtudiant
from memoires.models import Memoire
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role == 'etudiant':
            return Application.objects.filter(student__user=user)
        elif user.role in ['enseignant', 'superviseur']:
            return Application.objects.filter(subject__encadrant__user=user)
        return Application.objects.all()
    def get_permissions(self):
        if self.action == 'create':
            return [IsEtudiant()]
        return [IsAuthenticated()]
    @action(detail=True, methods=['post'], permission_classes=[IsEnseignant])
    def accept(self, request, pk=None):
        application = self.get_object()
        if application.statut != 'en_attente':
            return Response({'error': 'Candidature deja traitee.'}, status=status.HTTP_400_BAD_REQUEST)
        application.statut = 'acceptee'
        application.save()
        Memoire.objects.create(student=application.student, subject=application.subject)
        subject = application.subject
        if subject.applications.filter(statut='acceptee').count() >= subject.capacite:
            subject.statut = 'complet'
            subject.save()
        return Response({'message': 'Candidature acceptee. Memoire cree.'})
    @action(detail=True, methods=['post'], permission_classes=[IsEnseignant])
    def reject(self, request, pk=None):
        application = self.get_object()
        if application.statut != 'en_attente':
            return Response({'error': 'Candidature deja traitee.'}, status=status.HTTP_400_BAD_REQUEST)
        application.statut = 'refusee'
        application.save()
        return Response({'message': 'Candidature refusee.'})
    @action(detail=True, methods=['post'], permission_classes=[IsEtudiant])
    def cancel(self, request, pk=None):
        application = self.get_object()
        if application.statut != 'en_attente':
            return Response({'error': 'Impossible d\'annuler.'}, status=status.HTTP_400_BAD_REQUEST)
        application.delete()
        return Response({'message': 'Candidature annulee.'})
