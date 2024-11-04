import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db import transaction


class Command(BaseCommand):
    help = 'Imports groups and permissions from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=str, help='The CSV file to import groups and permissions from')

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                group_permissions = {}

                for row in reader:
                    group_name = row.get('Group Name')
                    codename = row.get('Codename')

                    if group_name and codename:
                        group_permissions.setdefault(
                            group_name, set()).add(codename)

                for group_name, permissions in group_permissions.items():
                    group, created = Group.objects.get_or_create(
                        name=group_name)

                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f'Created new group: {group_name}'))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f'Updating existing group: {group_name}'))

                    group.permissions.clear()
                    for codename in permissions:
                        try:
                            permission = Permission.objects.get(
                                codename=codename)
                            group.permissions.add(permission)
                        except Permission.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Permission with codename "{
                                              codename}" does not exist. Skipping.'))

                    group.save()
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully set permissions for group: {group_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'File "{csv_file_path}" not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
