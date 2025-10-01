from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'national_id', 'email', 'is_active']
    list_filter = ['gender', 'blood_type', 'is_active']
    search_fields = ['first_name', 'last_name', 'national_id', 'email']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'record_type', 'name', 'status', 'diagnosis_date']
    list_filter = ['record_type', 'status']
    search_fields = ['patient__first_name', 'patient__last_name', 'name']
