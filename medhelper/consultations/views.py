from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Consultation
from .serializers import ConsultationSerializer, ConsultationStatusSerializer
from .permissions import IsDoctorOrAdmin, IsPatientOrAdmin


class ConsultationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'start_time']
    search_fields = [
        'doctor__user__first_name',
        'doctor__user__last_name',
        'patient__user__first_name',
        'patient__user__last_name'
    ]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'DOCTOR':
            return Consultation.objects.filter(doctor=user.doctor_profile)
        elif user.role == 'PATIENT':
            return Consultation.objects.filter(patient=user.patient_profile)
        return Consultation.objects.all()


class ConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrAdmin | IsPatientOrAdmin]
    authentication_classes = [JWTAuthentication]


class ConsultationStatusUpdateView(generics.UpdateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrAdmin]
    authentication_classes = [JWTAuthentication]
