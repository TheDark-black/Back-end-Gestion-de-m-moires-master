from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
class IsResponsable(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'responsable']
class IsEnseignant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'responsable', 'enseignant', 'superviseur']
class IsEtudiant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'etudiant'
