import uuid
from django.db import models


class AcademicYear(models.Model):
    """
    Représente une année académique (ex: 2025-2026).
    Toutes les activités (sujets, soutenances) sont rattachées à une année.
    """

    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('archivee', 'Archivée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=20)           # ex: "2025-2026"
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')

    class Meta:
        db_table = 'academic_years'
        ordering = ['-date_debut']

    def __str__(self):
        return self.libelle


class Semester(models.Model):
    """
    Semestre rattaché à une année académique.
    Contient les dates limites clés (dépôt sujets, candidatures, documents).
    Le statut 'ouvert' ou 'ferme' contrôle si les étudiants peuvent candidater.
    """

    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('ferme', 'Fermé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='semesters'
    )
    libelle = models.CharField(max_length=50)           # ex: "Semestre 2 - 2025/2026"
    date_limite_sujets = models.DateField(null=True, blank=True)        # Limite proposition sujets
    date_limite_candidatures = models.DateField(null=True, blank=True)  # Limite candidature étudiants
    date_limite_documents = models.DateField(null=True, blank=True)     # Limite dépôt documents
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ferme')

    class Meta:
        db_table = 'semesters'
        ordering = ['academic_year', 'libelle']

    def __str__(self):
        return f"{self.libelle} ({self.academic_year})"

    @property
    def est_ouvert(self):
        """Retourne True si le semestre est ouvert aux candidatures."""
        return self.statut == 'ouvert'
