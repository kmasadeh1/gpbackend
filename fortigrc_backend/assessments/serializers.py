from rest_framework import serializers
from .models import Assessment, Evidence

class EvidenceSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Evidence
        fields = ['id', 'file', 'description', 'uploaded_at', 'file_name']

    def get_file_name(self, obj):
        return obj.file.name.split('/')[-1]

class AssessmentSerializer(serializers.ModelSerializer):
    evidence = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'control', 'status', 'notes', 'updated_at', 'evidence']
