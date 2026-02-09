from django.core.management.base import BaseCommand
from framework.models import Domain, SubDomain, Control

class Command(BaseCommand):
    help = 'Seeds the database with the Jordanian National Cybersecurity Framework (JNCSF)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding JNCSF data...')

        # 1. Clear existing data to prevent duplicates
        Control.objects.all().delete()
        SubDomain.objects.all().delete()
        Domain.objects.all().delete()

        # 2. Define Data Structure
        # (This is a representative subset. You can expand this list later.)
        framework_data = [
            {
                "code": "1",
                "name": "Governance and Strategy",
                "description": "Establish the governance framework and cybersecurity strategy.",
                "subdomains": [
                    {
                        "code": "1.1",
                        "name": "Cybersecurity Governance",
                        "controls": [
                            {"code": "1.1.1", "title": "Cybersecurity Roles & Responsibilities", "description": "Define and assign cybersecurity roles."},
                            {"code": "1.1.2", "title": "Cybersecurity Strategy", "description": "Develop and maintain a cybersecurity strategy."}
                        ]
                    },
                    {
                        "code": "1.2",
                        "name": "Risk Management",
                        "controls": [
                            {"code": "1.2.1", "title": "Risk Management Framework", "description": "Establish a risk management methodology."},
                            {"code": "1.2.2", "title": "Asset Management", "description": "Identify and classify information assets."}
                        ]
                    }
                ]
            },
            {
                "code": "2",
                "name": "Protection",
                "description": "Implement controls to ensure delivery of critical services.",
                "subdomains": [
                    {
                        "code": "2.1",
                        "name": "Access Control",
                        "controls": [
                            {"code": "2.1.1", "title": "Identity Management", "description": "Manage user identities and credentials."},
                            {"code": "2.1.2", "title": "Privileged Access Management", "description": "Restrict and monitor privileged access."}
                        ]
                    },
                    {
                        "code": "2.2",
                        "name": "Network Security",
                        "controls": [
                            {"code": "2.2.1", "title": "Network Segregation", "description": "Segregate networks based on trust levels."},
                            {"code": "2.2.2", "title": "Firewall Configuration", "description": "Manage firewall rules and configurations."}
                        ]
                    }
                ]
            },
            {
                "code": "3",
                "name": "Detection",
                "description": "Detect cybersecurity events.",
                "subdomains": [
                    {
                        "code": "3.1",
                        "name": "Monitoring",
                        "controls": [
                            {"code": "3.1.1", "title": "Security Logging", "description": "Enable and retain security logs."},
                            {"code": "3.1.2", "title": "Anomaly Detection", "description": "Detect anomalous activities."}
                        ]
                    }
                ]
            }
        ]

        # 3. Iterate and Create
        for d_data in framework_data:
            domain = Domain.objects.create(
                code=d_data['code'],
                name=d_data['name'],
                description=d_data['description']
            )
            self.stdout.write(f'Created Domain: {domain}')

            for s_data in d_data['subdomains']:
                sub = SubDomain.objects.create(
                    domain=domain,
                    code=s_data['code'],
                    name=s_data['name']
                )
                
                for c_data in s_data['controls']:
                    Control.objects.create(
                        sub_domain=sub,
                        code=c_data['code'],
                        title=c_data['title'],
                        description=c_data['description'],
                        maturity_level=1
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded JNCSF data.'))
