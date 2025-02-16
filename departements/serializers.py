from rest_framework import serializers

from enspd_webapp_api_auth.models import UserMember
from .models import Departement, Specialite, Cours, Lecon

class DepartementSerializer(serializers.ModelSerializer):
    # chef_de_departement = serializers.IntegerField(required=True)
    chef_de_departement = serializers.PrimaryKeyRelatedField(queryset=UserMember.objects.filter(status='Professeur'))
    nom_prof = serializers.CharField(source='chef_de_departement.username', read_only=True)
    class Meta:
        model = Departement
        fields = ['id', 'nom', 'chef_de_departement', 'nom_prof']

class SpecialitySerializer(serializers.ModelSerializer):
    nom_dep = serializers.CharField(source='departement.nom', read_only=True)
    class Meta:
        model = Specialite
        fields = ['id', 'nom', 'departement', 'nom_dep']

class CourseSerializer(serializers.ModelSerializer):
    nom_professeur = serializers.PrimaryKeyRelatedField(queryset=UserMember.objects.filter(status='Professeur'))
    speciality_nom = serializers.CharField(source='specialite.nom', read_only=True)
    professeur_enseignant = serializers.CharField(source='nom_professeur.username', read_only=True)
    class Meta:
        model = Cours
        fields = ['id', 'nom', 'specialite', 'nom_professeur', 'speciality_nom', 'professeur_enseignant']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecon
        fields = ['id', 'titre', 'contenu', 'cours']
