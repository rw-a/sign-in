import csv
from django.core.management.base import BaseCommand
from signin.models import Person


class Command(BaseCommand):
    help = "Loads people from a CSV file and adds them to the database. " \
           "CSV headers should be 'name', 'emergency_contact_name', 'emergency_contact_phone_number'"

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help="The name of the CSV file. Should end with .csv")

    def handle(self, *args, **options):
        people = []
        with open(options['filename'], 'w') as file:
            writer = csv.DictWriter(file,
                                    fieldnames=["name", "emergency_contact_name",
                                                "emergency_contact_phone_number", "media_permission"])
            writer.writeheader()
            for person in Person.objects.all():
                person_dict = {
                    "name": person.name,
                    "emergency_contact_name": person.emergency_contact_name,
                    "emergency_contact_phone_number": person.emergency_contact_phone_number,
                    "media_permission": person.media_permission
                }
                writer.writerow(person_dict)
                people.append(person.name)
        self.stdout.write(self.style.SUCCESS(f"Successfully exported to {options['filename']}.\n\n"
                                             f"The following people were included:\n{', '.join(people)}\n"))

