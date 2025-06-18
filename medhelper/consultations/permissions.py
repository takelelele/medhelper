from rest_framework import permissions


class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['DOCTOR', 'ADMIN']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        return obj.doctor.user == request.user


class IsPatientOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['PATIENT', 'ADMIN']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        return obj.patient.user == request.user
