from django.contrib import admin
from .models import Departement, Specialite, Cours, Lecon

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'chef_de_departement')
    search_fields = ('nom',)

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement')
    search_fields = ('nom',)
    list_filter = ('departement',)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'specialite', 'nom_professeur')
    search_fields = ('nom',)
    list_filter = ('specialite',)

@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours')
    search_fields = ('titre',)
    list_filter = ('cours',)
