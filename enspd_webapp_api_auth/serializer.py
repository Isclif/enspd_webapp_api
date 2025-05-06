from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .models import Department, Course, Enrollment, Content, Evaluation, Question, Result, ActivityReport, Speciality

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


class SpecialitySerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    # head_name = serializers.CharField(source='head.username', read_only=True)
    
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'description', 'department', 'department_name']
    
    def get_department_name(self, obj):
        return obj.department.name

class DepartmentSerializerList(serializers.ModelSerializer):
    head_name = serializers.SerializerMethodField()
    specialitys = SpecialitySerializer(many=True, read_only=True) 

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'head_name', 'specialitys']
    
    def get_head_name(self, obj):
        return obj.head.username
    
class DepartmentSerializer(serializers.ModelSerializer):
    specialitys = SpecialitySerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    course_data = serializers.SerializerMethodField() 
    class Meta:
        model = Content
        fields = ['id', 'course', 'title', 'type', 'content', 'course_data']
    
    def get_course_data(self, obj):
        return {
            "id": obj.course.id,
            "name": obj.course.name,
            "instructor": obj.course.instructor.username,
            "speciality": obj.course.speciality.name,
            'instructor_id':obj.course.instructor.id
        }

class EnrollmentSerializer(serializers.ModelSerializer):
    student_data = serializers.SerializerMethodField() 
    course_data = serializers.SerializerMethodField() 

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_data', 'course_data']
    
    def get_student_data(self, obj):
        return {
            "id": obj.student.id,
            "username": obj.student.username
        }
    
    def get_course_data(self, obj):
        return {
            "id": obj.course.id,
            "name": obj.course.name,
            'speciality':obj.course.speciality.name,
            'instructor':obj.course.instructor.username,
            'instructor_id':obj.course.instructor.id,
            "dept_name": obj.course.speciality.department.name
        }
    
class CourseSerializer(serializers.ModelSerializer):
    # speciality_name = serializers.CharField(source='speciality.name', read_only=True)
    contents = ContentSerializer(many=True, read_only=True)
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    
    speciality_data = serializers.SerializerMethodField() 
    instructor_name = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'speciality', 'instructor', 'instructor_name', 'speciality_data', 'contents', 'enrollments']
    
    def get_instructor_name(self, obj):
        return obj.instructor.username
    
    def get_speciality_data(self, obj):
        return {
            "id": obj.speciality.id,
            "name": obj.speciality.name,
            "dept_name": obj.speciality.department.name
        }


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        

class ActivityRepportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityReport
        fields = '__all__'