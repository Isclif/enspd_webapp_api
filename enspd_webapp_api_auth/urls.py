from django.urls import path
from .views import AddPermissionsAPIView, ListEtudiantsAPIView, ListProfesseursAPIView, ListUsersAPIView, RegisterAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('add-permissions/', AddPermissionsAPIView.as_view(), name='add_permissions'),
    path('list-users/', ListUsersAPIView.as_view(), name='list_users'),
    path('list-etudiants/', ListEtudiantsAPIView.as_view(), name='list_etudiants'),
    path('list-professeurs/', ListProfesseursAPIView.as_view(), name='list_professeurs'),
]
