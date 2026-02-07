from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Domain, Control
from .serializers import DomainSerializer
from assessments.models import Assessment
from risks.models import Risk

class FrameworkListView(generics.ListAPIView):
    queryset = Domain.objects.prefetch_related('sub_domains__controls').all()
    serializer_class = DomainSerializer
    pagination_class = None # Return full tree structure

class DashboardStatsView(APIView):
    def get(self, request):
        # Compliance Stats
        total_controls = Control.objects.count()
        compliant_controls = Assessment.objects.filter(status=Assessment.Status.COMPLIANT).count()
        compliance_percentage = (compliant_controls / total_controls * 100) if total_controls > 0 else 0

        # Assessment Breakdown
        stats_not_started = Assessment.objects.filter(status=Assessment.Status.NOT_STARTED).count()
        # "Not Started" implicitly includes controls without assessments.
        # However, if we assume 1:1, we can just say total - exists?
        # Actually Assessment is OneToOne with Control. So if an assessment doesn't exist, it's effectively "Not Started".
        # But for now, let's rely on the Assessment model existing or not.
        # Requirement said: "Count of "Not Started" (Total Controls - Existing Assessments)"?
        # Re-reading req: "Count of "Not Started" (Total Controls - Existing Assessments)."
        # Wait, if Assessment is created only when someone starts it?
        # Or do we create them all at once?
        # If we assume we don't pre-create:
        assessments_count = Assessment.objects.count()
        implicit_not_started = total_controls - assessments_count
        explicit_not_started = Assessment.objects.filter(status=Assessment.Status.NOT_STARTED).count()
        total_not_started = implicit_not_started + explicit_not_started

        in_progress = Assessment.objects.filter(status=Assessment.Status.IN_PROGRESS).count()
        non_compliant = Assessment.objects.filter(status=Assessment.Status.NON_COMPLIANT).count()

        # Risk Stats
        total_risks = Risk.objects.count()
        high_risks = Risk.objects.filter(risk_score__gte=16).count()
        medium_risks = Risk.objects.filter(risk_score__range=(9, 15)).count()
        low_risks = Risk.objects.filter(risk_score__lte=8).count()

        data = {
            "compliance": {
                "total_controls": total_controls,
                "compliant_controls": compliant_controls,
                "compliance_percentage": round(compliance_percentage, 2)
            },
            "assessments": {
                "not_started": total_not_started,
                "in_progress": in_progress,
                "non_compliant": non_compliant
            },
            "risks": {
                "total_risks": total_risks,
                "high_risks": high_risks,
                "medium_risks": medium_risks,
                "low_risks": low_risks
            }
        }
        return Response(data)
