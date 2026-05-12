from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Teacher, Student
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'nom', 'prenom', 'role', 'is_active', 'is_staff', 'created_at']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['email', 'nom', 'prenom']
    ordering = ['-created_at']
    fieldsets = (
        ('Connexion', {'fields': ('email', 'password')}),
        ('Identite', {'fields': ('nom', 'prenom', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'nom', 'prenom', 'role', 'password1', 'password2')}),
    )
    readonly_fields = ['created_at', 'last_login']
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_nom', 'get_prenom', 'get_email', 'grade', 'specialite']
    list_filter = ['grade']
    search_fields = ['user__nom', 'user__prenom', 'user__email']
    def get_nom(self, obj): return obj.user.nom
    get_nom.short_description = 'Nom'
    def get_prenom(self, obj): return obj.user.prenom
    get_prenom.short_description = 'Prenom'
    def get_email(self, obj): return obj.user.email
    get_email.short_description = 'Email'
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'get_nom', 'get_prenom', 'promotion', 'master']
    list_filter = ['promotion', 'master']
    search_fields = ['matricule', 'user__nom', 'user__prenom']
    def get_nom(self, obj): return obj.user.nom
    get_nom.short_description = 'Nom'
    def get_prenom(self, obj): return obj.user.prenom
    get_prenom.short_description = 'Prenom'
