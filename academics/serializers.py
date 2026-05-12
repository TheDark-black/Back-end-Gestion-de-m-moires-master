from rest_framework import serializers
from .models import AcademicYear, Semester
class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
class AcademicYearSerializer(serializers.ModelSerializer):
    semesters = SemesterSerializer(many=True, read_only=True)
    class Meta:
        model = AcademicYear
        fields = ['id', 'libelle', 'date_debut', 'date_fin', 'statut', 'semesters']
