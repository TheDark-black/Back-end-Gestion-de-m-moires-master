from rest_framework import serializers
from .models import Application
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'student', 'subject', 'motivation', 'date_candidature', 'statut']
        read_only_fields = ['id', 'date_candidature', 'statut']
    def validate(self, data):
        student = data.get('student')
        if Application.objects.filter(student=student, statut='acceptee').exists():
            raise serializers.ValidationError(
                "Vous avez deja une candidature acceptee."
            )
        if Application.objects.filter(student=student, statut='en_attente').exists():
            raise serializers.ValidationError(
                "Vous avez deja une candidature en attente. Annulez-la d'abord."
            )
        subject = data.get('subject')
        if subject and subject.statut != 'publie':
            raise serializers.ValidationError("Ce sujet n'est plus disponible.")
        return data
