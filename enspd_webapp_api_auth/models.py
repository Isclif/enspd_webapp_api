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
    status = models.CharField(max_length=30, choices=STATUT)
    speciality = models.CharField(max_length=50)
    sexe = models.CharField(max_length=10, choices=SEXE, default="e")

    class Meta:
        ordering = ["last_name", "first_name"]
    
    def __str__(self):
        return self.username 
    
    updated_by = models.CharField(max_length=255, null = True, blank = True)


class Department(BaseUUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    head = models.ForeignKey(UserMember, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name
    
class Speciality(BaseUUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='specialitys')

    def __str__(self):
        return self.name

class Course(BaseUUIDModel):
    name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(UserMember, on_delete=models.CASCADE, related_name='instructor_courses')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Enrollment(BaseUUIDModel):
    student = models.ForeignKey(UserMember, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Content(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    content = models.CharField(max_length=2024, null=True, blank=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Evaluation(BaseUUIDModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='evaluations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(BaseUUIDModel):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.evaluation.title} - {self.text}"

class Result(BaseUUIDModel):
    student = models.ForeignKey(UserMember, on_delete=models.CASCADE, related_name='results')
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='results')
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - {self.evaluation.title} - {self.score}"
    

class ActivityReport(BaseUUIDModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserMember, on_delete=models.CASCADE, related_name='activities_reports')

    def __str__(self):
        return f"{self.user.username} - {self.name}"

