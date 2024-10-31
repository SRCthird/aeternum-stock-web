import csv
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export all Django groups with their permissions to a CSV file'

    def handle(self, *args, **kwargs):
        # Retrieve all groups with their permissions
        groups = Group.objects.prefetch_related('permissions').all()

        # Define the file path for the CSV
        file_path = 'groups_permissions.csv'

        # Open the CSV file and write group-permission data
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['Group Name', 'Permission Name',
                            'Codename', 'Content Type'])

            # Write data rows
            for group in groups:
                for perm in group.permissions.all():
                    writer.writerow([
                        group.name,
                        perm.name,
                        perm.codename,
                        perm.content_type
                    ])

        self.stdout.write(self.style.SUCCESS(
            f'Groups and permissions exported to {file_path}'))
