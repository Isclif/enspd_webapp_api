from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from enspd_webapp_api.constants import SEXE, STATUT
from enspd_webapp_api.models import BaseUUIDModel
from django.core.validators import RegexValidator

# Create your models here.

class UserMember(BaseUUIDModel, AbstractUser):

    
    matricule = models.CharField(max_length=50, unique=True)    
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés.")]
    )
    status = models.CharField(max_length=10, choices=STATUT)
    speciality = models.CharField(max_length=50)
    sexe = models.CharField(max_length=10, choices=SEXE, default="e")

    class Meta:
        ordering = ["last_name", "first_name"]
    
    def __str__(self):
        return self.username 
