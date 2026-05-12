from rest_framework import serializers
from .models import Memoire, Milestone, Document, Observation
class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'
        read_only_fields = ['id']
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'date_depot']
class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'
        read_only_fields = ['id', 'date_observation', 'auteur']
class MemoireSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    observations = ObservationSerializer(many=True, read_only=True)
    class Meta:
        model = Memoire
        fields = ['id', 'student', 'subject', 'date_affectation',
                  'statut_avancement', 'soutenable', 'date_validation_soutenabilite',
                  'milestones', 'documents', 'observations']
        read_only_fields = ['id', 'date_affectation', 'student', 'subject', 'soutenable']
