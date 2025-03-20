from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from enspd_webapp_api_auth.serializer import UserMemberSerializer, UserMemberSerializerLogin, ListEtudiantsProfesseursSerializer


from rest_framework import status
from rest_framework.views import APIView
from enspd_webapp_api_auth.models import UserMember
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

UserMember = get_user_model()

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

class ListUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.all()
        serializer = UserMemberSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListEtudiantsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if not request.user.status == "Professeur" and not request.user.is_superuser == True:
        #     return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.filter(status="Etudiant")
        serializer = ListEtudiantsProfesseursSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListProfesseursAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if not request.user.is_superuser:
        #     return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        users = UserMember.objects.filter(status="Professeur")
        serializer = ListEtudiantsProfesseursSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)