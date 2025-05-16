from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from enspd_webapp_api_auth.serializer import ( 
    ResultCreateSerializer,
    UserMemberSerializer, 
    UserMemberSerializerLogin, 
    ListEtudiantsProfesseursSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    ResultSerializer,
    ContentSerializer,
    DepartmentSerializer,
    SpecialitySerializer,
    ActivityRepportSerializer,
    DepartmentSerializerList, 
    EvaluationSerializer,
    QuestionSerializer
)


from rest_framework import status
from rest_framework.views import APIView
from enspd_webapp_api_auth.models import UserMember, Department, Course, Enrollment, Result, Content, Speciality, ActivityReport, Evaluation, Question
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .permissions import IsDepartmentHead, IsInstructor, IsStudent

UserMember = get_user_model()

# def is_user_in_group(user_id, group_name):
#     user = UserMember.objects.get(id=user_id)
#     return user.groups.filter(name=group_name).exists()

class UserInfoView(APIView):
    """
    View to retrieve user information from the token.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"success": True, "data":{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff
        }}, status=status.HTTP_200_OK)
    

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserMemberSerializerLogin(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            try:
                validate_password(password)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            user = UserMember.objects.create_user(
                username=serializer.validated_data['username'],
                matricule=serializer.validated_data.get('matricule'),
                telephone=serializer.validated_data.get('telephone'),
                status=serializer.validated_data.get('status'),
                speciality=serializer.validated_data.get('speciality'),
                password=password,
                first_name=serializer.validated_data.get('first_name'),
                last_name=serializer.validated_data.get('last_name'),
                email=serializer.validated_data.get('email'),
                sexe=serializer.validated_data.get('sexe'),
            )

            refresh = RefreshToken.for_user(user)
            return Response({"message":"Compte creer avec success !!!"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            try:
                user = UserMember.objects.get(username=username)
                return Response({'error': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            except UserMember.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        response = super().post(request, *args, **kwargs)
        data = response.data
        data['user'] = UserMemberSerializer(user).data
        return Response(data)


class AddPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_superuser == False:
            return Response({'error': 'Only admin are allowed to add permissions using this endpoint.'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        permissions = request.data.get('permissions', [])

        if not username or not permissions:
            return Response({'error': 'Username and permissions are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserMember.objects.get(username=username)
        except UserMember.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                user.user_permissions.add(permission)
            except Permission.DoesNotExist:
                return Response({'error': f'Permission {perm} not found'}, status=status.HTTP_404_NOT_FOUND)

        user.save()
        return Response({'success': 'Permissions added successfully'}, status=status.HTTP_200_OK)

class UsersAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.all()
        serializer = UserMemberSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EtudiantsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if not request.user.status == "Professeur" and not request.user.is_superuser == True:
        #     return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.filter(status="Etudiant")
        serializer = ListEtudiantsProfesseursSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfesseursAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if not request.user.is_superuser:
        #     return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.filter(status="Professeur")
        serializer = ListEtudiantsProfesseursSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user

        if pk:
            instance = get_object_or_404(Course, pk=pk)

            # Check permission
            # self.check_object_permissions(request, instance)

            serializer = CourseSerializer(instance)
            return Response({"success": True, "data":serializer.data}, status=status.HTTP_200_OK)
        else:

            # Vérifier si l'utilisateur est un admin
            if user.is_superuser:
                # Un admin peut voir tous les cours
                courses = Course.objects.all()
            elif IsDepartmentHead().has_permission(request, self):
                # Le chef de département peut voir tous les cours de son département
                department = Department.objects.filter(head=user).first()
                courses = Course.objects.filter(instructor=department.head)
            elif IsInstructor().has_permission(request, self):
                # L'enseignant ne peut voir que ses propres cours
                courses = Course.objects.filter(instructor=user)
            elif user.status == "Etudiant":
                courses = Course.objects.all()
            else:
                return Response({"error": "Unauthorized"}, status=403)

            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    def post(self, request):
        # Seul le chef de département et les admins peuvent créer un cours
        if not (request.user.is_superuser or IsDepartmentHead().has_permission(request, self)):
            return Response({"error": "Only department heads and admin can create courses"}, status=403)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EnrollmentView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        # Inscription d'un étudiant à un cours
        course_id = request.data.get('course_id')
        student = request.user

        if student.status != "Etudiant":
            return Response({"message": "Unauthorize to register to a course with a non student account"}, status=403)

        if not course_id:
            return Response({"error": "Course ID is required"}, status=400)

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            return Response({"message": "Enrollment successful"}, status=201)
        return Response({"message": "Already enrolled"}, status=200)

    def get(self, request):
        # Liste des cours auxquels l'étudiant est inscrit
        student = request.user
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    

class ResultView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsInstructor]

    def get(self, request, pk=None):
        user = request.user

        if IsStudent().has_permission(request, self):
            # Un étudiant ne peut voir que ses propres résultats
            results = Result.objects.filter(student=user)
        elif IsInstructor().has_permission(request, self):
            # Un enseignant peut voir les résultats des étudiants inscrits à ses cours
            instructor_courses = Course.objects.filter(instructor=user)
            results = Result.objects.filter(evaluation__course__in=instructor_courses)
        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user

        # # Récupérer le cours spécifié par course_id
        # try:
        #     course = Course.objects.get(id=course_id)
        # except Course.DoesNotExist:
        #     return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est l'enseignant assigné à ce cours
        if not (user.status == "Etudiant"):
            return Response({"error": "Only student can pass this evaluation"}, status=status.HTTP_403_FORBIDDEN)

        # Ajouter le cours au contenu
        # request.data['course'] = course.id

        # Sérialiser les données reçues
        serializer = ResultCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            evaluation = serializer.validated_data['evaluation']

            try:

                existing_result = Result.objects.filter(student=user, evaluation=evaluation).first()

                print("connected_user", user)
                # print("existing_result", existing_result)

                if existing_result:
                    # raise ValidationError("Cet étudiant est déjà inscrit à cette évaluation.")
                    return Response({
                        'detail': 'Cet étudiant est déjà inscrit à cette évaluation.',
                        'result_id': existing_result.id,
                        'evaluation_id': existing_result.evaluation.id
                    }, status=status.HTTP_409_CONFLICT)
                
                serializer.save(student=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # Une autre requête a créé le même Result en parallèle
                existing_result = Result.objects.filter(student=user, evaluation=evaluation).first()
                return Response({
                    'detail': 'Cet étudiant est déjà inscrit à cette évaluation.',
                    'result_id': existing_result.id if existing_result else None,
                    'evaluation_id': existing_result.evaluation.id
                }, status=status.HTTP_409_CONFLICT)

            # existing_result = Result.objects.filter(student=user, evaluation=evaluation).first()

            # print("existing_result", existing_result)

            # if existing_result:
            #     # raise ValidationError("Cet étudiant est déjà inscrit à cette évaluation.")
            #     return Response({
            #         'detail': 'Cet étudiant est déjà inscrit à cette évaluation.',
            #         'result_id': existing_result.id,
            #         'evaluation_id': existing_result.evaluation.id
            #     }, status=status.HTTP_409_CONFLICT)
            
            # serializer.save(student=user)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = request.user

        result_eval = get_object_or_404(Result, pk=pk)

        if not (user.status == "Etudiant"):
            return Response({"error": "Only student can update this evaluation"}, status=status.HTTP_403_FORBIDDEN)
        
        # Sérialiser les données reçues avec partial=True pour permettre des mises à jour partielles
        serializer = ResultSerializer(result_eval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvaluationView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsInstructor]

    def get(self, request, pk=None):
        user = request.user

        if IsStudent().has_permission(request, self):
            # Un étudiant ne peut voir que ses propres résultats
            courses = Enrollment.objects.filter(student=user).values_list('course', flat=True)
            results = Evaluation.objects.filter(course__in=courses)
        elif IsInstructor().has_permission(request, self):
            # Un enseignant peut voir les résultats des étudiants inscrits à ses cours
            instructor_courses = Course.objects.filter(instructor=user)
            results = Evaluation.objects.filter(course__in=instructor_courses)
        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = EvaluationSerializer(results, many=True)
        return Response(serializer.data)
    
    def post(self, request, course_id):
        user = request.user

        # Récupérer le cours spécifié par course_id
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est l'enseignant assigné à ce cours
        if not (course.instructor == user):
            return Response({"error": "Only the assigned instructor can create evaluation"}, status=status.HTTP_403_FORBIDDEN)

        # Ajouter le cours au contenu
        # request.data['course'] = course.id

        # Sérialiser les données reçues
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(autor=user, course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = request.user

        evaluation = get_object_or_404(Evaluation, pk=pk)

        if not (evaluation.course.instructor == user):
            return Response(
                {"error": "Only the assigned instructor can update evaluation"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Sérialiser les données reçues avec partial=True pour permettre des mises à jour partielles
        serializer = EvaluationSerializer(evaluation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionsView(APIView):
    permission_classes = [IsAuthenticated, IsStudent | IsInstructor]

    def get(self, request, pk=None):
        user = request.user

        # if IsStudent().has_permission(request, self):
        #     # Un étudiant ne peut voir que ses propres résultats
        #     courses = Enrollment.objects.filter(student=user).values_list('course', flat=True)
        #     results = Question.objects.filter(evaluation__course__in=courses)
        if IsInstructor().has_permission(request, self):
            # Un enseignant peut voir les résultats des étudiants inscrits à ses cours
            instructor_courses = Course.objects.filter(instructor=user)
            results = Question.objects.filter(evaluation__course__in=instructor_courses)
        else:
            return Response({"error": "Unauthorized"}, status=403)

        serializer = QuestionSerializer(results, many=True)
        return Response(serializer.data)
    
    def post(self, request, course_id):
        user = request.user

        # Récupérer le cours spécifié par course_id
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est l'enseignant assigné à ce cours
        if not (user.is_superuser or (course.instructor == user)):
            return Response({"error": "Only the assigned instructor or admin can create questions on an evaluation"}, status=status.HTTP_403_FORBIDDEN)

        # Ajouter le cours au contenu
        # request.data['course'] = course.id

        # Sérialiser les données reçues
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = request.user

        question = get_object_or_404(Question, pk=pk)

        if not ((question.evaluation.course.instructor == user)):
            return Response(
                {"error": "Only the assigned instructor or admin can update questions"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Sérialiser les données reçues avec partial=True pour permettre des mises à jour partielles
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user

        # Récupérer le cours spécifié par course_id
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si l'utilisateur est l'enseignant assigné à ce cours
        if not (user.is_superuser or (course.instructor == user)):
            return Response({"error": "Only the assigned instructor or admin can create content for this course"}, status=status.HTTP_403_FORBIDDEN)

        # Ajouter le cours au contenu
        # request.data['course'] = course.id

        # Sérialiser les données reçues
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        user = request.user

        if pk:
            instance = get_object_or_404(Content, pk=pk)

            # Check permission
            # self.check_object_permissions(request, instance)

            serializer = ContentSerializer(instance)
            return Response({"success": True, "data":serializer.data}, status=status.HTTP_200_OK)
        else:

            # Vérifier si l'utilisateur est un admin
            if user.is_superuser:
                # Un admin peut voir tous les contenus de cours
                contents = Content.objects.all()
            elif IsDepartmentHead().has_permission(request, self):
                # Le chef de département peut voir tous les contenus de cours
                # department = Department.objects.get(head=user)
                contents = Content.objects.all()
            # elif IsInstructor().has_permission(request, self):
            #     # L'enseignant ne peut voir que ses propres cours
            #     courses = Course.objects.filter(instructor=user).first()
            #     contents = Content.objects.filter(course=courses.id)
            elif user.status == "Etudiant":
                contents = Content.objects.all()
            else:
                return Response({"error": "Unauthorized"}, status=403)

            serializer = ContentSerializer(contents, many=True)
            return Response(serializer.data)
    
    def patch(self, request, pk):
        user = request.user

        content = get_object_or_404(Content, pk=pk)

        # Vérifier si l'utilisateur est l'enseignant assigné à ce cours
        print("content.course.instructor", content.course.instructor)
        if not (user.is_superuser or (content.course.instructor == user)):
            return Response(
                {"error": "Only the assigned instructor or admin can update content for this course"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Sérialiser les données reçues avec partial=True pour permettre des mises à jour partielles
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Vérifier si l'utilisateur est un admin ou un chef de département
        if not (user.is_superuser or IsDepartmentHead().has_permission(request, self)):
            return Response({"error": "Only admins or department heads can create departments"}, status=status.HTTP_403_FORBIDDEN)

        # Sérialiser les données reçues
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            # Assigner automatiquement le chef du département (si ce n'est pas un admin)
            if not user.is_superuser:
                serializer.validated_data['head'] = user  # Le créateur devient le chef du département
            serializer.save()

            # Récupérer le groupe
            group_name = "DepartmentHead"
            group, created = Group.objects.get_or_create(name=group_name)

            user_head = UserMember.objects.filter(username=serializer.validated_data['head']).first()

            # # Ajouter l'utilisateur au groupe
            user_head.groups.add(group)
            user_head.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        # Liste departements

        if pk:
            instance = get_object_or_404(Department, pk=pk)

            # Check permission
            # self.check_object_permissions(request, instance)

            serializer = DepartmentSerializerList(instance)
            return Response({"success": True, "data":serializer.data}, status=status.HTTP_200_OK)
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializerList(departments, many=True)
            return Response(serializer.data)
            # return Response(
            #     {
            #         "success": True,
            #         "data": paginated_response.data,
            #     },
            #     status=status.HTTP_200_OK
            # )
    
class SpecialityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Vérifier si l'utilisateur est un admin ou un chef de département
        if not (user.is_superuser or IsDepartmentHead().has_permission(request, self)):
            return Response({"error": "Only admins or department heads can create specialities"}, status=status.HTTP_403_FORBIDDEN)

        # Sérialiser les données reçues
        serializer = SpecialitySerializer(data=request.data)
        if serializer.is_valid():
            # Assigner automatiquement le chef du département (si ce n'est pas un admin)
            # if not user.is_superuser:
            #     serializer.validated_data['head'] = user  # Le créateur devient le chef du département
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Liste departements
        departments = Speciality.objects.all()
        serializer = SpecialitySerializer(departments, many=True)
        return Response(serializer.data)


class ActivityRepportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not (user.status == "Professeur" or user.status == "ChefDepartement"):
            return Response({"error": "Only admins or department heads can create activity reports"}, status=status.HTTP_403_FORBIDDEN)

        # Sérialiser les données reçues
        serializer = ActivityRepportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Liste rapports d'activités
        activity_repports = ActivityReport.objects.all()
        serializer = SpecialitySerializer(activity_repports, many=True)
        return Response(serializer.data)

class AddUserToGroup(APIView):

    permission_classes = [IsAuthenticated]

    def post(request):
        # Récupérer les données de la requête
        user_id = request.data.get('user_id')
        group_name = request.data.get('group_name')

        if not request.user.is_superuser:
            return Response({"error": "Unauthorized, only for superuser"}, status=403)

        if not user_id or not group_name:
            return Response({"error": "Les champs 'user_id' et 'group_name' sont requis."}, status=400)

        try:
            user = UserMember.objects.get(id=user_id)
        except UserMember.DoesNotExist:
            return Response({"error": "L'utilisateur spécifié n'existe pas."}, status=404)

        # Récupérer le groupe
        group, created = Group.objects.get_or_create(name=group_name)

        # Ajouter l'utilisateur au groupe
        user.groups.add(group)
        user.save()

        return Response({"message": f"L'utilisateur {user.username} a été ajouté au groupe {group_name}."})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])