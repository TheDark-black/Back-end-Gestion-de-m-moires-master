import uuid
from django.db import models
from accounts.models import Student, User
from subjects.models import Subject


class Memoire(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('suspendu', 'Suspendu'),
        ('abandonne', 'Abandonné'),
        ('finalise', 'Finalisé'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='memoire')
    subject = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name='memoire')
    date_affectation = models.DateTimeField(auto_now_add=True)
    statut_avancement = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    soutenable = models.BooleanField(default=False)
    date_validation_soutenabilite = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'memoires'

    def __str__(self):
        return f"Memoire de {self.student} - {self.subject.titre}"


class Milestone(models.Model):
    STATUT_CHOICES = [
        ('a_faire', 'A faire'),
        ('en_cours', 'En cours'),
        ('valide', 'Valide'),
        ('depasse', 'Depasse'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memoire = models.ForeignKey(Memoire, on_delete=models.CASCADE, related_name='milestones')
    libelle = models.CharField(max_length=150)
    echeance = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_faire')

    class Meta:
        db_table = 'milestones'

    def __str__(self):
        return f"{self.libelle} [{self.statut}]"


class Document(models.Model):
    TYPE_CHOICES = [
        ('plan', 'Plan'),
        ('version_intermediaire', 'Version intermediaire'),
        ('version_finale', 'Version finale'),
        ('annexe', 'Annexe'),
        ('fiche_validation', 'Fiche de validation'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memoire = models.ForeignKey(Memoire, on_delete=models.CASCADE, related_name='documents')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    nom_fichier = models.CharField(max_length=255)
    chemin_stockage = models.CharField(max_length=500)
    version = models.IntegerField(default=1)
    date_depot = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documents'

    def __str__(self):
        return f"{self.nom_fichier} (v{self.version})"


class Observation(models.Model):
    TYPE_CHOICES = [
        ('commentaire', 'Commentaire'),
        ('recommandation', 'Recommandation'),
        ('correction', 'Correction'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memoire = models.ForeignKey(Memoire, on_delete=models.CASCADE, related_name='observations')
    auteur = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='observations_ecrites')
    contenu = models.TextField()
    type_observation = models.CharField(max_length=30, choices=TYPE_CHOICES, null=True, blank=True)
    date_observation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'observations'

    def __str__(self):
        return f"Obs. de {self.auteur}"
