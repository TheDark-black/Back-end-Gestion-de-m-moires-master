from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_etudiant', 'subject', 'statut', 'date_candidature']
    list_filter = ['statut', 'subject__semester']
    search_fields = ['student__user__nom', 'student__user__prenom', 'subject__titre']
    readonly_fields = ['date_candidature']

    def get_etudiant(self, obj):
        return f"{obj.student.user.prenom} {obj.student.user.nom}"
    get_etudiant.short_description = 'Etudiant'
