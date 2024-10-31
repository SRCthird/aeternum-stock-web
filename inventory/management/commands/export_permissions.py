import csv
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export all Django permissions to a CSV file'

    def handle(self, *args, **kwargs):
        # Retrieve all permissions
        permissions = Permission.objects.all()

        # Define the file path for the CSV
        file_path = 'permissions.csv'

        # Open the CSV file and write permissions data
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['ID', 'Name', 'Codename', 'Content Type'])

            # Write data rows
            for perm in permissions:
                writer.writerow(
                    [perm.id, perm.name, perm.codename, perm.content_type])

        self.stdout.write(self.style.SUCCESS(
            f'Permissions exported to {file_path}'))
