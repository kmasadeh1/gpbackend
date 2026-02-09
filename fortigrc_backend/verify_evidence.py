import os
import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortigrc_backend.settings')
django.setup()

from rest_framework.test import APIRequestFactory
from assessments.models import Assessment, Evidence
from assessments.serializers import AssessmentSerializer
from framework.models import Control, SubDomain, Domain
from django.contrib.auth import get_user_model

User = get_user_model()

def verify_evidence_serialization():
    print("Verifying Evidence Serialization...")

    # 1. Setup Data
    # Ensure we have a user
    user, _ = User.objects.get_or_create(username='test_auditor', email='test@example.com', defaults={'role': 'Auditor'})
    
    # Ensure we have a control (assuming seeded data exists, or create one)
    domain, _ = Domain.objects.get_or_create(code='TEST', name='Test Domain')
    sub, _ = SubDomain.objects.get_or_create(domain=domain, code='TEST.1', name='Test Sub')
    control, _ = Control.objects.get_or_create(sub_domain=sub, code='TEST.1.1', title='Test Control')

    # Create Assessment
    assessment, _ = Assessment.objects.get_or_create(control=control, auditor=user, defaults={'status': 'Pending'})

    # Create Evidence
    dummy_file = SimpleUploadedFile("test_evidence.txt", b"dummy content")
    evidence = Evidence.objects.create(assessment=assessment, file=dummy_file, description="Test Evidence")

    print(f"Created Assessment: {assessment.id}")
    print(f"Created Evidence: {evidence.id}")

    # 2. Serialize
    serializer = AssessmentSerializer(assessment)
    data = serializer.data

    # 3. Check Evidence
    if 'evidence' in data:
        evidence_list = data['evidence']
        print(f"Evidence field found. Count: {len(evidence_list)}")
        if len(evidence_list) > 0:
            first_evidence = evidence_list[0]
            print(f"Evidence Data: {first_evidence}")
            if first_evidence['id'] == evidence.id and first_evidence['description'] == "Test Evidence":
                print("SUCCESS: Evidence correctly nested in Assessment serialization.")
            else:
                print("FAILURE: Evidence data mismatch.")
        else:
            print("FAILURE: Evidence list is empty.")
    else:
        print("FAILURE: 'evidence' field missing in serialized data.")

    # Cleanup
    evidence.delete()
    # Don't delete assessment/control to avoid cascading delete issues if other things use them, 
    # or just leave them as test artifacts. For this script, we'll leave them.

if __name__ == "__main__":
    verify_evidence_serialization()
