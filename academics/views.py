from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AcademicYear, Semester
from .serializers import AcademicYearSerializer, SemesterSerializer
from common.permissions import IsResponsable
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [IsAuthenticated()]
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.select_related('academic_year').all()
    serializer_class = SemesterSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsResponsable()]
        return [IsAuthenticated()]
