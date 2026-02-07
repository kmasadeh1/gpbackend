from rest_framework import viewsets, parsers
from .models import Assessment, Evidence
from .serializers import AssessmentSerializer, EvidenceSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
