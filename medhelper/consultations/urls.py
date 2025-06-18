from django.urls import path
from .views import (
    ConsultationListCreateView,
    ConsultationRetrieveUpdateDestroyView,
    ConsultationStatusUpdateView,
)

urlpatterns = [
    path('', ConsultationListCreateView.as_view(), name='consultation-list'),
    path('<int:pk>/', ConsultationRetrieveUpdateDestroyView.as_view(), name='consultation-detail'),
    path('<int:pk>/status/', ConsultationStatusUpdateView.as_view(), name='consultation-status-update'),
]
