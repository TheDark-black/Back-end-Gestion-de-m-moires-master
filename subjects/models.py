import uuid
from django.db import models
from academics.models import Semester
from accounts.models import Teacher


class Subject(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('complet', 'Complet'),
        ('archive', 'Archivé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    resume = models.TextField(blank=True, null=True)
    objectifs = models.TextField(blank=True, null=True)
    competences_requises = models.TextField(blank=True, null=True)
    mots_cles = models.CharField(max_length=255, blank=True, null=True)
    encadrant = models.ForeignKey(Teacher, on_delete=models.RESTRICT, related_name='sujets_encadres')
    superviseur = models.ForeignKey(Teacher, on_delete=models.RESTRICT, related_name='sujets_supervises')
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT, related_name='subjects')
    capacite = models.IntegerField(default=1)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.titre