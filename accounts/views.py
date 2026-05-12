from rest_framework import viewsets, status
from rest_framework.views import APIView  
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Teacher, Student
from .serializers import UserSerializer, UserCreateSerializer, TeacherSerializer, StudentSerializer, LoginSerializer
from common.permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode








def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}
class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({'user': UserSerializer(user).data, 'tokens': tokens})
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
        except Exception:
            pass
        return Response({'message': 'Deconnexion reussie.'})
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'list']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]
    

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # En prod : envoyer un vrai email
            # En dev : on retourne le lien directement
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"
            return Response({
                'message': 'Lien de réinitialisation généré.',
                'reset_link': reset_link  # À supprimer en production
            })
        except User.DoesNotExist:
            # On ne révèle pas si l'email existe ou non
            return Response({'message': 'Si cet email existe, un lien a été envoyé.'})

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            from django.utils.http import urlsafe_base64_decode
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Mot de passe réinitialisé avec succès.'})
            else:
                return Response({'error': 'Token invalide ou expiré.'}, status=400)
        except Exception:
            return Response({'error': 'Requête invalide.'}, status=400)    


