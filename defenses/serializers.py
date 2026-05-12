from rest_framework import serializers
from .models import DefenseSession, Defense, Jury, JuryMember, DefenseObservation, Grade
class DefenseSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefenseSession
        fields = '__all__'
class DefenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defense
        fields = '__all__'
        read_only_fields = ['id']
    def validate(self, data):
        memoire = data.get('memoire')
        if memoire and not memoire.soutenable:
            raise serializers.ValidationError(
                "Ce memoire n'est pas marque comme soutenable par l'encadrant."
            )
        return data
class JuryMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuryMember
        fields = '__all__'
class JurySerializer(serializers.ModelSerializer):
    members = JuryMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Jury
        fields = ['id', 'defense', 'members']
class DefenseObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefenseObservation
        fields = '__all__'
        read_only_fields = ['auteur']
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['id', 'date_saisie', 'mention']
    def validate(self, data):
        defense = data.get('defense')
        if defense and not defense.tenue_effective:
            raise serializers.ValidationError(
                "La soutenance n'a pas encore eu lieu. La note ne peut pas etre saisie."
            )
        return data
