from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import UserMember, Departement, Specialite, Cours, Lecon
from .serializers import DepartementSerializer, SpecialitySerializer, CourseSerializer, LessonSerializer

class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    permission_classes = [IsAuthenticated]

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Specialite.objects.all()
    serializer_class = SpecialitySerializer
    permission_classes = [IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lecon.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

