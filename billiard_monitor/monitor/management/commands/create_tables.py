from django.core.management.base import BaseCommand
from monitor.models import Table

class Command(BaseCommand):
    help = 'Create initial billiard tables'

    def handle(self, *args, **options):
        # Create 8 tables
        for i in range(1, 9):
            Table.objects.get_or_create(
                table_number=i,
                defaults={'status': 'available'}
            )
        self.stdout.write(self.style.SUCCESS('Successfully created 8 tables'))