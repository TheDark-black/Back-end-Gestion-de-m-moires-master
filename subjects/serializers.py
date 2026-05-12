from rest_framework import serializers
from .models import Subject
GRADES_SUPERVISEUR = ['Maitre_Conferences', 'Professeur']
class SubjectSerializer(serializers.ModelSerializer):
    nb_candidatures = serializers.SerializerMethodField()
    class Meta:
        model = Subject
        fields = ['id', 'titre', 'resume', 'objectifs', 'competences_requises',
                  'mots_cles', 'encadrant', 'superviseur', 'semester',
                  'capacite', 'statut', 'nb_candidatures']
    def get_nb_candidatures(self, obj):
        return obj.applications.count()
    def validate_superviseur(self, value):
        if value.grade not in GRADES_SUPERVISEUR:
            raise serializers.ValidationError(
                "Le superviseur doit avoir au moins le grade de Maitre de Conferences."
            )
        return value
    def validate(self, data):
        if data.get('encadrant') and data.get('superviseur'):
            if data['encadrant'] == data['superviseur']:
                raise serializers.ValidationError(
                    "L'encadrant et le superviseur doivent etre des personnes differentes."
                )
        return data
