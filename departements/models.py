from django.db import models
from django.conf import settings
from enspd_webapp_api.models import BaseUUIDModel
from enspd_webapp_api_auth.models import UserMember  # Assurez-vous que le chemin est correct

class Departement(BaseUUIDModel):
    nom = models.CharField(max_length=100)
    chef_de_departement = models.ForeignKey(
        UserMember, 
        limit_choices_to={'status': 'Professeur'},
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='prof'
    )

    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['nom']

class Specialite(BaseUUIDModel):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='specialites')

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']

class Cours(BaseUUIDModel):
    nom = models.CharField(max_length=100)
    nom_professeur = models.ForeignKey(
        UserMember, 
        limit_choices_to={'status': 'Professeur'},
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='cours_professeur'
    )
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, related_name='cours_specialite')

    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['nom']

class Lecon(BaseUUIDModel):
    titre = models.CharField(max_length=100)
    contenu = models.TextField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='lecons')

    def __str__(self):
        return self.titre
    
    class Meta:
        ordering = ['titre']
