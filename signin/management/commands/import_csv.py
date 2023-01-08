import csv
from django.core.management.base import BaseCommand, CommandError
from signin.models import Person


class Command(BaseCommand):
    help = "Loads people from a CSV file and adds them to the database. " \
           "CSV headers should be 'name', 'emergency_contact_name', 'emergency_contact_phone_number'"

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help="The name of the CSV file. Should end with .csv")

    def handle(self, *args, **options):
        try:
            with open(options['filename']) as file:
                reader = csv.DictReader(file)
                people = []
                for row in reader:
                    people.append(row["name"])
                    person = Person(name=row["name"],
                                    emergency_contact_name=row["emergency_contact_name"],
                                    emergency_contact_phone_number=row["emergency_contact_phone_number"])
                    person.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {options['filename']}. "
                                                 f"The following people were added:\n{', '.join(people)}"))
        except FileNotFoundError:
            with open(options['filename'], 'w') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["name", "emergency_contact_name", "emergency_contact_phone_number"])
                writer.writeheader()
            self.stdout.write(self.style.WARNING(f"{options['filename']} not found, so an empty CSV with that name "
                                                 f"was created."))
