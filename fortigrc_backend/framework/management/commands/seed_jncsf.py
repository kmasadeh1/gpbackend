from django.core.management.base import BaseCommand
from framework.models import Domain, SubDomain, Control
from risks.models import Asset

class Command(BaseCommand):
    help = 'Seeds the database with initial JNCSF framework data and dummy assets.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Cleaning old data...'))
        
        # Clear existing data to prevent duplicates
        # Order matters for deletion due to foreign keys if not relying on CASCADE
        Control.objects.all().delete()
        SubDomain.objects.all().delete()
        Domain.objects.all().delete()
        Asset.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Old data cleaned.'))
        
        self.stdout.write(self.style.WARNING('Seeding framework data...'))
        
        # Create 1 Domain
        domain = Domain.objects.create(
            name="Governance & Strategy",
            code="1",
            description="Domain covering governance and strategic alignment."
        )
        
        # Create 1 SubDomain linked to the Domain
        sub_domain = SubDomain.objects.create(
            domain=domain,
            name="Governance",
            code="1.1"
        )
        
        # Create 3 Controls linked to the SubDomain
        Control.objects.create(
            sub_domain=sub_domain,
            code="1.1.1",
            title="Cybersecurity Strategy",
            description="Establishment and maintenance of a cybersecurity strategy.",
            maturity_level=1
        )
        Control.objects.create(
            sub_domain=sub_domain,
            code="1.1.2",
            title="Roles and Responsibilities",
            description="Definition and allocation of cybersecurity roles.",
            maturity_level=1
        )
        Control.objects.create(
            sub_domain=sub_domain,
            code="1.1.3",
            title="Legal and Regulatory Compliance",
            description="Compliance with applicable legal and regulatory requirements.",
            maturity_level=1
        )
        
        self.stdout.write(self.style.SUCCESS('Framework seeded.'))
        
        self.stdout.write(self.style.WARNING('Seeding assets...'))
        
        # Create 3 Assets
        # Note: Asset values are from choices in risks.models.Asset.Value
        Asset.objects.create(
            name="HR Database",
            value=Asset.Value.HIGH,
            description="Database containing sensitive employee information."
        )
        Asset.objects.create(
            name="Corporate Website",
            value=Asset.Value.MEDIUM,
            description="Public facing corporate website."
        )
        Asset.objects.create(
            name="Payment Gateway",
            value=Asset.Value.HIGH,
            description="External payment processing gateway integration."
        )
        
        self.stdout.write(self.style.SUCCESS('Assets seeded.'))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
