from django.contrib import admin
from .models import AcademicYear, Semester
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'date_debut', 'date_fin', 'statut']
    list_filter = ['statut']
    search_fields = ['libelle']
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'academic_year', 'statut', 'date_limite_sujets', 'date_limite_candidatures']
    list_filter = ['statut', 'academic_year']
    search_fields = ['libelle']
