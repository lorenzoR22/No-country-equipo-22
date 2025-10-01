from django.db import models

# Create your models here.
import uuid
from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('U', 'No especificado'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(unique=True)  # From Auth Service
    
    # Personal Information
    national_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=100, blank=True)
    
    # Insurance Information
    insurance_provider = models.CharField(max_length=255, blank=True)
    insurance_number = models.CharField(max_length=100, blank=True)
    insurance_type = models.CharField(max_length=100, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    
    # Medical Information
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'patients'
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['national_id']),
            models.Index(fields=['first_name', 'last_name']),
        ]
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.national_id}"

class MedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('allergy', 'Alergia'),
        ('condition', 'Condición Médica'),
        ('medication', 'Medicamento'),
        ('procedure', 'Procedimiento'),
        ('vaccination', 'Vacuna'),
        ('test_result', 'Resultado de Examen'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('resolved', 'Resuelto'),
        ('chronic', 'Crónico'),
        ('inactive', 'Inactivo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    
    record_type = models.CharField(max_length=50, choices=RECORD_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    diagnosis_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    severity = models.CharField(max_length=50, blank=True)  # mild, moderate, severe
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        indexes = [
            models.Index(fields=['patient', 'record_type']),
        ]
        ordering = ['-diagnosis_date', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.patient}"