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
        assessments_count = Assessment.objects.count()
        implicit_not_started = total_controls - assessments_count
        explicit_not_started = Assessment.objects.filter(status=Assessment.Status.NOT_STARTED).count()
        total_not_started = implicit_not_started + explicit_not_started

        in_progress = Assessment.objects.filter(status=Assessment.Status.IN_PROGRESS).count()
        non_compliant = Assessment.objects.filter(status=Assessment.Status.NON_COMPLIANT).count()

        # Risk Stats (Active/Open Only)
        active_risks = Risk.objects.filter(status=Risk.Status.OPEN)

        total_risks = active_risks.count()
        high_risks = active_risks.filter(risk_score__gte=16).count()
        medium_risks = active_risks.filter(risk_score__range=(9, 15)).count()
        low_risks = active_risks.filter(risk_score__lte=8).count()
        
        # Add a stat for mitigated risks to show progress
        mitigated_risks = Risk.objects.filter(status=Risk.Status.MITIGATED).count()

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
                "low_risks": low_risks,
                "mitigated": mitigated_risks # New field
            }
        }
        return Response(data)

class ExecutiveReportView(APIView):
    def get(self, request):
        # 1. Compliance Score
        total_controls = Control.objects.count()
        compliant_controls = Assessment.objects.filter(status=Assessment.Status.COMPLIANT).count()
        compliance_percentage = (compliant_controls / total_controls * 100) if total_controls > 0 else 0

        # 2. Risk Summary (Active/Open Only)
        active_risks = Risk.objects.filter(status=Risk.Status.OPEN)

        low_risks = active_risks.filter(risk_score__lte=8).count()
        medium_risks = active_risks.filter(risk_score__range=(9, 15)).count()
        high_risks = active_risks.filter(risk_score__gte=16).count()

        # 3. Top 5 Risks (Active Only)
        top_risks = active_risks.order_by('-risk_score')[:5]
        top_risks_data = [
            {
                "threat": risk.threat,
                "asset_name": risk.asset.name, # Added asset name
                "likelihood": risk.likelihood,
                "impact": risk.impact,
                "risk_score": risk.risk_score
            }
            for risk in top_risks
        ]

        # 4. Top 5 Compliance Gaps (Non-Compliant Assessments)
        # Note: We can order by updated_at or similar to show recent issues, or just any
        compliance_gaps = Assessment.objects.filter(status=Assessment.Status.NON_COMPLIANT)[:5]
        compliance_gaps_data = [
            {
                "control_code": gap.control.code,
                "control_title": gap.control.title
            }
            for gap in compliance_gaps
        ]

        data = {
            "compliance_score": round(compliance_percentage, 2),
            "risk_summary": {
                "low": low_risks,
                "medium": medium_risks,
                "high": high_risks
            },
            "top_risks": top_risks_data,
            "compliance_gaps": compliance_gaps_data
        }
        return Response(data)
