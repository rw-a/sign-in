import csv
from django.core.management.base import BaseCommand
from signin.models import Person


class Command(BaseCommand):
    help = "Loads people from a CSV file and adds them to the database. " \
           "CSV headers should be 'name', 'emergency_contact_name', 'emergency_contact_phone_number'"

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help="The name of the CSV file. Should end with .csv")

    def handle(self, *args, **options):
        try:
            with open(options['filename'], 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                people_added = []
                people_existed = []

                for row in reader:
                    # strip inputs (remove trailing whitespaces on start and end)
                    name = row["name"].strip()
                    emergency_contact_name = row["emergency_contact_name"].strip()
                    emergency_contact_phone_number = row["emergency_contact_phone_number"].strip()

                    # don't do anything if the person already exists
                    if Person.objects.filter(name=name).exists():
                        people_existed.append(name)
                        continue

                    if len(emergency_contact_phone_number) > 0 and emergency_contact_phone_number[0] == '4':
                        emergency_contact_phone_number = '0' + emergency_contact_phone_number

                    person = Person(
                        name=name,
                        emergency_contact_name=emergency_contact_name,
                        emergency_contact_phone_number=emergency_contact_phone_number
                    )

                    if row["media_permission"].lower() in ['yes', 'true']:
                        person.media_permission = True

                    person.save()
                    people_added.append(name)

            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {options['filename']}.\n\n"
                                                 f"The following people were added:\n{', '.join(people_added)}\n"))
            self.stdout.write(self.style.NOTICE(f"The following people already existed, so nothing was changed:"
                                                f"\n{', '.join(people_existed)}"))
        except FileNotFoundError:
            with open(options['filename'], 'w') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["name", "emergency_contact_name", "emergency_contact_phone_number",
                                                    "media_permission"])
                writer.writeheader()
            self.stdout.write(self.style.WARNING(f"{options['filename']} not found, so an empty CSV with that name "
                                                 f"was created."))
