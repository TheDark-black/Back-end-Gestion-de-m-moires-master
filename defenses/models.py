import uuid
from django.db import models
from accounts.models import Teacher, User
from memoires.models import Memoire
from academics.models import Semester


class DefenseSession(models.Model):
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=150, blank=True, null=True)
    date_session = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    salle = models.CharField(max_length=100, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT, related_name='defense_sessions')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')

    class Meta:
        db_table = 'defense_sessions'

    def __str__(self):
        return f"{self.libelle or 'Session'} - {self.date_session}"


class Defense(models.Model):
    STATUT_CHOICES = [
        ('programmee', 'Programmée'),
        ('tenue', 'Tenue'),
        ('annulee', 'Annulée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memoire = models.OneToOneField(Memoire, on_delete=models.CASCADE, related_name='defense')
    session = models.ForeignKey(DefenseSession, on_delete=models.RESTRICT, related_name='defenses')
    tenue_effective = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='programmee')
    date_heure = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'defenses'

    def __str__(self):
        return f"Soutenance de {self.memoire.student}"


class Jury(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    defense = models.OneToOneField(Defense, on_delete=models.CASCADE, related_name='jury')

    class Meta:
        db_table = 'juries'

    def __str__(self):
        return f"Jury - {self.defense}"


class JuryMember(models.Model):
    ROLE_CHOICES = [
        ('president', 'Président'),
        ('encadrant', 'Encadrant'),
        ('superviseur', 'Superviseur'),
        ('membre', 'Membre'),
        ('rapporteur', 'Rapporteur'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jury = models.ForeignKey(Jury, on_delete=models.CASCADE, related_name='members')
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT, related_name='jury_participations')
    role_dans_jury = models.CharField(max_length=30, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'jury_members'
        unique_together = [('jury', 'teacher')]

    def __str__(self):
        return f"{self.teacher} - {self.role_dans_jury}"


class DefenseObservation(models.Model):
    CRITERE_CHOICES = [
        ('qualite_scientifique', 'Qualité scientifique'),
        ('qualite_redactionnelle', 'Qualité rédactionnelle'),
        ('presentation_orale', 'Présentation orale'),
        ('maitrise_sujet', 'Maîtrise du sujet'),
        ('recommandations', 'Recommandations'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    defense = models.ForeignKey(Defense, on_delete=models.CASCADE, related_name='defense_observations')
    auteur = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='defense_observations_ecrites')
    contenu = models.TextField()
    critere = models.CharField(max_length=50, choices=CRITERE_CHOICES, null=True, blank=True)

    class Meta:
        db_table = 'defense_observations'


class Grade(models.Model):
    MENTION_CHOICES = [
        ('Passable', 'Passable'),
        ('Assez_Bien', 'Assez Bien'),
        ('Bien', 'Bien'),
        ('Tres_Bien', 'Très Bien'),
        ('Excellent', 'Excellent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    defense = models.OneToOneField(Defense, on_delete=models.CASCADE, related_name='grade')
    note_document = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_travail = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_presentation = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_reponses = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    note_finale = models.DecimalField(max_digits=4, decimal_places=2)
    mention = models.CharField(max_length=30, choices=MENTION_CHOICES, null=True, blank=True)
    commentaires = models.TextField(blank=True, null=True)
    validee = models.BooleanField(default=False)
    date_saisie = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grades'

    def save(self, *args, **kwargs):
        note = float(self.note_finale)
        if note >= 18:
            self.mention = 'Excellent'
        elif note >= 16:
            self.mention = 'Tres_Bien'
        elif note >= 14:
            self.mention = 'Bien'
        elif note >= 12:
            self.mention = 'Assez_Bien'
        else:
            self.mention = 'Passable'
        super().save(*args, **kwargs)