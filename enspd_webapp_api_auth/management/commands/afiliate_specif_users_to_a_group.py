from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from enspd_webapp_api_auth.models import UserMember

class Command(BaseCommand):
    help = "Crée les groupes 'Student', 'Instructor' et 'DepartmentHead' si ils n'existent pas."

    def handle(self, *args, **options):
        # Créer les groupes
        student_group, created_student = Group.objects.get_or_create(name='Student')
        instructor_group, created_instructor = Group.objects.get_or_create(name='Instructor')
        department_head_group, created_department_head = Group.objects.get_or_create(name='DepartmentHead')

        students_users = UserMember.objects.filter(status="Etudiant")
        if students_users:
            for user in students_users:
                # Ajouter l'utilisateur au groupe
                user.groups.add(student_group)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"l'etudiant {user.username} ajouté avec succès au groupe {student_group.name}."))


        instructor_users = UserMember.objects.filter(status="Professeur")
        if instructor_users:
            for user in instructor_users:
                # Ajouter l'utilisateur au groupe
                user.groups.add(instructor_group)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"le professeur {user.username} ajouté avec succès au groupe {instructor_group.name}."))


        department_head_users = UserMember.objects.filter(status="ChefDepartement")
        if department_head_users:
            for user in department_head_users:
                # Ajouter l'utilisateur au groupe
                user.groups.add(department_head_group)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"le chef de depart {user.username} ajouté avec succès au groupe {department_head_group.name}."))
