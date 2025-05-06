
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Student').exists()

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Instructor').exists()

class IsDepartmentHead(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='DepartmentHead').exists()