from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['titre', 'encadrant', 'superviseur', 'semester', 'statut', 'capacite', 'nb_candidatures_count']
    list_filter = ['statut', 'semester']
    search_fields = ['titre', 'mots_cles', 'encadrant__user__nom']

    def nb_candidatures_count(self, obj):
        return obj.applications.count()
    nb_candidatures_count.short_description = 'Candidatures'
