from django.contrib import admin
from .models import Memoire, Milestone, Document, Observation


class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0
    fields = ['libelle', 'echeance', 'statut']


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    fields = ['type', 'nom_fichier', 'version', 'date_depot']
    readonly_fields = ['date_depot']


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0
    fields = ['auteur', 'type_observation', 'contenu', 'date_observation']
    readonly_fields = ['date_observation']


@admin.register(Memoire)
class MemoireAdmin(admin.ModelAdmin):
    list_display = ['get_etudiant', 'get_sujet', 'statut_avancement', 'soutenable', 'date_affectation']
    list_filter = ['statut_avancement', 'soutenable']
    search_fields = ['student__user__nom', 'subject__titre']
    readonly_fields = ['date_affectation', 'date_validation_soutenabilite']
    inlines = [MilestoneInline, DocumentInline, ObservationInline]

    def get_etudiant(self, obj):
        return f"{obj.student.user.prenom} {obj.student.user.nom}"
    get_etudiant.short_description = 'Etudiant'

    def get_sujet(self, obj):
        return obj.subject.titre[:60]
    get_sujet.short_description = 'Sujet'


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'memoire', 'echeance', 'statut']
    list_filter = ['statut']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['nom_fichier', 'memoire', 'type', 'version', 'date_depot']
    list_filter = ['type']
    readonly_fields = ['date_depot']


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'memoire', 'type_observation', 'date_observation']
    list_filter = ['type_observation']
    readonly_fields = ['date_observation']
