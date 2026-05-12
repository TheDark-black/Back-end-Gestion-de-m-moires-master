from django.contrib import admin
from .models import DefenseSession, Defense, Jury, JuryMember, DefenseObservation, Grade


class JuryMemberInline(admin.TabularInline):
    model = JuryMember
    extra = 0
    fields = ['teacher', 'role_dans_jury']


@admin.register(DefenseSession)
class DefenseSessionAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'date_session', 'heure_debut', 'heure_fin', 'salle', 'semester', 'statut']
    list_filter = ['statut', 'semester']
    search_fields = ['libelle', 'salle']


@admin.register(Defense)
class DefenseAdmin(admin.ModelAdmin):
    list_display = ['get_etudiant', 'session', 'date_heure', 'statut', 'tenue_effective']
    list_filter = ['statut', 'tenue_effective']
    search_fields = ['memoire__student__user__nom']
    readonly_fields = ['memoire']

    def get_etudiant(self, obj):
        return f"{obj.memoire.student.user.prenom} {obj.memoire.student.user.nom}"
    get_etudiant.short_description = 'Etudiant'


@admin.register(Jury)
class JuryAdmin(admin.ModelAdmin):
    list_display = ['defense', 'get_nb_membres']
    inlines = [JuryMemberInline]

    def get_nb_membres(self, obj):
        return obj.members.count()
    get_nb_membres.short_description = 'Nb membres'


@admin.register(JuryMember)
class JuryMemberAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'jury', 'role_dans_jury']
    list_filter = ['role_dans_jury']


@admin.register(DefenseObservation)
class DefenseObservationAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'defense', 'critere']
    list_filter = ['critere']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['defense', 'note_finale', 'mention', 'validee', 'date_saisie']
    list_filter = ['mention', 'validee']
    readonly_fields = ['date_saisie', 'mention']
