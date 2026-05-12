import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
        ('superviseur', 'Superviseur'),
        ('responsable', 'Responsable de Master'),
        ('admin', 'Administrateur'),
        ('jury', 'Membre de Jury'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"


class Teacher(models.Model):
    GRADE_CHOICES = [
        ('Assistant', 'Assistant'),
        ('Maitre_Assistant', 'Maître Assistant'),
        ('Maitre_Conferences', 'Maître de Conférences'),
        ('Professeur', 'Professeur'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    specialite = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} - {self.grade}"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matricule = models.CharField(max_length=50, unique=True)
    promotion = models.CharField(max_length=50, blank=True, null=True)
    master = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.matricule} - {self.user.prenom} {self.user.nom}"