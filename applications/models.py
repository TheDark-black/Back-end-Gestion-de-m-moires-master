import uuid
from django.db import models
from accounts.models import Student
from subjects.models import Subject


class Application(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='applications')
    motivation = models.TextField(blank=True, null=True)
    date_candidature = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        db_table = 'applications'
        unique_together = [('student', 'subject')]

    def __str__(self):
        return f"{self.student} → {self.subject} [{self.statut}]"