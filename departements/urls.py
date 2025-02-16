from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DepartementViewSet, SpecialityViewSet, CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'departements', DepartementViewSet)
router.register(r'specialities', SpecialityViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]