from rest_framework import serializers
from .models import Assessment, Evidence

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'assessment', 'file', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class AssessmentSerializer(serializers.ModelSerializer):
    evidence = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'control', 'auditor', 'status', 'notes', 'updated_at', 'evidence']
        read_only_fields = ['updated_at']
