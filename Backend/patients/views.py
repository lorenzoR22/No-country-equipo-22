from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

# ✅ Importaciones absolutas
from patients.models import Patient, MedicalRecord
from patients.serializers import (
    PatientSerializer, PatientCreateSerializer, 
    PatientUpdateSerializer, PatientListSerializer,
    MedicalRecordSerializer
)
class PatientListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['gender', 'blood_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'national_id', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['first_name']

    def get(self, request):
        user_role = request.user.get('role')
        user_id = request.user.get('user_id')
        
        # Patients can only see their own profile
        if user_role == 'PATIENT':
            patients = Patient.objects.filter(user_id=user_id)
        # Doctors and admins can see all patients
        elif user_role in ['DOCTOR', 'ADMIN']:
            patients = Patient.objects.all()
        else:
            patients = Patient.objects.none()
        
        # Apply filtering and searching
        patients = self.filter_queryset(patients)
        
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_role = request.user.get('role')
        
        # Only admins or system can create patients
        if user_role not in ['ADMIN', 'SYSTEM']:
            return Response(
                {'error': 'No tienes permisos para crear pacientes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientCreateSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(
                PatientSerializer(patient).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class PatientDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check permissions
        if not self._has_permission(request, patient):
            return Response(
                {'error': 'No tienes permisos para ver este paciente'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check permissions
        if not self._has_permission(request, patient, for_update=True):
            return Response(
                {'error': 'No tienes permisos para editar este paciente'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PatientUpdateSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            patient = serializer.save()
            return Response(PatientSerializer(patient).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _has_permission(self, request, patient, for_update=False):
        user_role = request.user.get('role')
        user_id = request.user.get('user_id')
        
        if user_role == 'PATIENT':
            return str(patient.user_id) == user_id
        elif user_role in ['DOCTOR', 'ADMIN']:
            return True
        return False

class PatientMedicalRecordsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check permissions
        if not self._has_permission(request, patient):
            return Response(
                {'error': 'No tienes permisos para ver el historial médico'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        records = patient.medical_records.all()
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, patient_id):
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Paciente no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Only doctors and admins can add medical records
        user_role = request.user.get('role')
        if user_role not in ['DOCTOR', 'ADMIN']:
            return Response(
                {'error': 'No tienes permisos para agregar registros médicos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _has_permission(self, request, patient):
        user_role = request.user.get('role')
        user_id = request.user.get('user_id')
        
        if user_role == 'PATIENT':
            return str(patient.user_id) == user_id
        elif user_role in ['DOCTOR', 'ADMIN']:
            return True
        return False

class PatientSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        user_role = request.user.get('role')
        
        if not query or len(query) < 3:
            return Response(
                {'error': 'La búsqueda debe tener al menos 3 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Only doctors and admins can search patients
        if user_role not in ['DOCTOR', 'ADMIN']:
            return Response(
                {'error': 'No tienes permisos para buscar pacientes'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(national_id__icontains=query) |
            Q(email__icontains=query)
        ).filter(is_active=True)
        
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)