from django.core.management.base import BaseCommand
from framework.models import Domain, SubDomain, Control

class Command(BaseCommand):
    help = 'Seeds the database with initial JNCSF sample structure'

    def handle(self, *args, **options):
        if Domain.objects.exists():
            self.stdout.write(self.style.SUCCESS('Database already has data, skipping seed.'))
            return

        self.stdout.write('Seeding JNCSF data...')

        # 1. Create Domain
        gov = Domain.objects.create(
            name="Governance & Strategy",
            code="GOV",
            description="Governance encompasses the system by which an organization is directed and controlled."
        )

        # 2. Create SubDomain
        policy_sub = SubDomain.objects.create(
            domain=gov,
            name="Information Security Policies",
            code="1-1"
        )

        # 3. Create Controls
        controls_data = [
            {
                "code": "1-1-1",
                "title": "Develop an InfoSec Policy",
                "description": "Establish a set of policies for information security.",
                "maturity_level": 1
            },
            {
                "code": "1-1-2",
                "title": "Review Policy Annually",
                "description": "Review the policies at planned intervals or if significant changes occur.",
                "maturity_level": 2
            },
            {
                "code": "1-1-3",
                "title": "Approve Policy",
                "description": "Ensure the policy is approved by management.",
                "maturity_level": 3
            }
        ]

        for c_data in controls_data:
            Control.objects.create(sub_domain=policy_sub, **c_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded JNCSF sample data.'))
