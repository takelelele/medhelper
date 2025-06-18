import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounting.models import User
from consultations.models import Consultation, Doctor, Patient, Clinic


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username='admin',
        password='admin123',
        email='admin@example.com',
        role='ADMIN'
    )


@pytest.fixture
def doctor_user():
    user = User.objects.create_user(
        username='doctor',
        password='doctor123',
        first_name='John',
        last_name='Doe',
        role='DOCTOR'
    )
    Doctor.objects.create(user=user, specialization='Cardiologist')
    return user


@pytest.fixture
def patient_user():
    user = User.objects.create_user(
        username='patient',
        password='patient123',
        first_name='Jane',
        last_name='Smith',
        role='PATIENT'
    )
    Patient.objects.create(user=user, phone='1234567890', email='jane@example.com')
    return user


@pytest.fixture
def clinic():
    return Clinic.objects.create(
        name='City Hospital',
        legal_address='123 Main St',
        physical_address='123 Main St'
    )


@pytest.fixture
def consultation(doctor_user, patient_user, clinic):
    doctor = doctor_user.doctor_profile
    patient = patient_user.patient_profile
    return Consultation.objects.create(
        start_time='2023-01-01T10:00:00Z',
        end_time='2023-01-01T11:00:00Z',
        status='PENDING',
        doctor=doctor,
        patient=patient,
        clinic=clinic
    )


@pytest.mark.django_db
class TestConsultationAPI:
    def test_create_consultation_as_patient(self, api_client, patient_user, doctor_user, clinic):
        initial_count = Consultation.objects.count()

        api_client.force_authenticate(user=patient_user)
        doctor = doctor_user.doctor_profile
        patient = patient_user.patient_profile
        url = reverse('consultation-list')
        data = {
            'start_time': '2023-01-02T10:00:00Z',
            'end_time': '2023-01-02T11:00:00Z',
            'doctor': doctor.id,
            'patient': patient.id,
            'clinic': clinic.id,
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        assert Consultation.objects.count() == initial_count + 1

    def test_update_status_as_doctor(self, api_client, doctor_user, consultation):
        api_client.force_authenticate(user=doctor_user)
        url = reverse('consultation-status-update', kwargs={'pk': consultation.id})
        data = {'status': 'CONFIRMED'}
        response = api_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        consultation.refresh_from_db()
        assert consultation.status == 'CONFIRMED'

    def test_filter_consultations(self, api_client, admin_user, consultation):
        api_client.force_authenticate(user=admin_user)
        url = f"{reverse('consultation-list')}?status=PENDING"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
