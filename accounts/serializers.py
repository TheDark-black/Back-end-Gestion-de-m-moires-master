from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Teacher, Student
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'grade', 'specialite']
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'matricule', 'promotion', 'master']
class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)
    student_profile = StudentProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'role', 'is_active', 'created_at', 'teacher_profile', 'student_profile']
        read_only_fields = ['id', 'created_at']
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'password', 'role']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_id', 'grade', 'specialite']
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Student
        fields = ['id', 'user', 'user_id', 'matricule', 'promotion', 'master']
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est desactive.")
        data['user'] = user
        return data
