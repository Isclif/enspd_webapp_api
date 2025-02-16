from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from enspd_webapp_api.constants import SEXE

UserMember = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class UserMemberSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = UserMember
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'matricule', 'telephone', 'status', 'speciality', 'groups', 'user_permissions', 'is_active', 'is_superuser', 'sexe']


class UserMemberSerializerLogin(serializers.ModelSerializer):
    last_name = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    class Meta:
        model = UserMember
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'matricule', 'telephone', 'status', 'speciality', 'is_active', 'is_superuser', 'sexe']


class ListEtudiantsProfesseursSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMember
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'matricule', 'telephone', 'status', 'speciality', 'sexe']