import csv
from django.core.management.base import BaseCommand, CommandError
from signin.models import Person, Session


class Command(BaseCommand):
    help = "Imports people"

    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **options):
        with open(options["file"]) as file:
            reader = csv.DictReader(file)

            utime_9am = Session.objects.get(code="utime9")
            utime_11am = Session.objects.get(code="utime11")
            ufo = Session.objects.get(code="ufo")

            for row in reader:
                full_name = row["Child's Full Name"]
                emergency_contact_name = row["Emergency Contact Name"]
                emergency_contact_phone = row["Emergency Contact Phone"]
                media_permission = row["Media Permission"] == "Yes"
                is_utime_9am = row["U-Time 9am"] == "1"
                is_utime_11am = row["U-Time 11am"] == "1"
                is_ufo = row["UFO"] == "1"

                first_name = full_name.split(" ")[0]
                last_name = full_name.split(" ")[-1]
                emergency_contact_first_name = emergency_contact_name.split(" ")[0]
                emergency_contact_last_name = emergency_contact_name.split(" ")[1] \
                    if len(emergency_contact_name.split(" ")) > 1 else ""

                person = Person(
                    first_name=first_name,
                    last_name=last_name,
                    media_permission=media_permission,
                    emergency_contact_phone_number=emergency_contact_phone,
                    emergency_contact_first_name=emergency_contact_first_name,
                    emergency_contact_last_name=emergency_contact_last_name
                )

                person.save()

                if is_utime_9am:
                    person.sessions.add(utime_9am)
                if is_utime_11am:
                    person.sessions.add(utime_11am)
                if is_ufo:
                    person.sessions.add(ufo)

                person.save()

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded {full_name}")
                )

