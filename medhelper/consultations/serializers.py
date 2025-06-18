from rest_framework import serializers
from .models import Consultation, Doctor, Patient, Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'created_at', 'start_time', 'end_time', 'status',
            'doctor', 'doctor_name', 'patient', 'patient_name',
            'clinic', 'clinic_name'
        ]
        read_only_fields = ['created_at', 'status']


class ConsultationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['status']
