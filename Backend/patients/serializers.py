from rest_framework import serializers
from .models import Patient, MedicalRecord
from datetime import date

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    medical_records = MedicalRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('id', 'created_at', 'updated_at')
    
    def validate_national_id(self, value):
        if Patient.objects.filter(national_id=value).exists():
            raise serializers.ValidationError("Ya existe un paciente con este DNI")
        return value

class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('id', 'user_id', 'national_id', 'created_at', 'updated_at')

class PatientListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'user_id', 'national_id', 'full_name', 'age', 
            'gender', 'phone', 'email', 'blood_type', 'is_active'
        ]
    
    def get_age(self, obj):
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"