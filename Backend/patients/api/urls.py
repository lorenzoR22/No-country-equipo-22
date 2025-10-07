from django.urls import path
from patients.views import ( 
    PatientListCreateAPIView, 
    PatientDetailAPIView,
    PatientMedicalRecordsAPIView,
    PatientSearchAPIView
)

urlpatterns = [
    path('patients/', PatientListCreateAPIView.as_view(), name='patient-list-create'),
    path('patients/<uuid:pk>/', PatientDetailAPIView.as_view(), name='patient-detail'),
    path('patients/<uuid:patient_id>/medical-records/', PatientMedicalRecordsAPIView.as_view(), name='patient-medical-records'),
    path('patients/search/', PatientSearchAPIView.as_view(), name='patient-search'),
]