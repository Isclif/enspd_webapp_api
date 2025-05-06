from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Crée les groupes 'Student', 'Instructor' et 'DepartmentHead' si ils n'existent pas."

    def handle(self, *args, **options):
        # Créer les groupes
        student_group, created_student = Group.objects.get_or_create(name='Student')
        instructor_group, created_instructor = Group.objects.get_or_create(name='Instructor')
        department_head_group, created_department_head = Group.objects.get_or_create(name='DepartmentHead')

        # Afficher un message pour chaque groupe créé ou existant
        if created_student:
            self.stdout.write(self.style.SUCCESS("Groupe 'Student' créé avec succès."))
        else:
            self.stdout.write("Groupe 'Student' existe déjà.")

        if created_instructor:
            self.stdout.write(self.style.SUCCESS("Groupe 'Instructor' créé avec succès."))
        else:
            self.stdout.write("Groupe 'Instructor' existe déjà.")

        if created_department_head:
            self.stdout.write(self.style.SUCCESS("Groupe 'DepartmentHead' créé avec succès."))
        else:
            self.stdout.write("Groupe 'DepartmentHead' existe déjà.")