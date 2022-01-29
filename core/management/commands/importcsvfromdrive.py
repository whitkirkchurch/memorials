import requests
from contextlib import closing
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

from core.models import Location, Memorial, Name


class Command(BaseCommand):
    help = "Imports a CSV from the given URL"

    def add_arguments(self, parser):
        parser.add_argument("csv_url")

    def handle(self, *args, **options):

        with closing(requests.get(options["csv_url"], stream=True)) as r:
            f = (line.decode("utf-8") for line in r.iter_lines())
            reader = csv.DictReader(f)
            for row in reader:

                # Preflight checks!
                if row["Family Name"] == "" and row["Given Name"] == "":
                    continue

                try:

                    section = Location.objects.get(slug=row["Section"])

                    memorial, created = Memorial.objects.get_or_create(
                        plot_reference=row["Plot"],
                        location=section,
                        defaults={"complete": False, "published": True},
                    )

                    name, created = Name.objects.get_or_create(
                        import_key=row["Import Key"]
                    )

                    name.family_name = row["Family Name"].capitalize()
                    name.given_names = row["Given Name"]

                    if row["Aged"]:
                        if row["Aged"].isdigit():
                            name.died_aged = int(row["Aged"])
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    '{} Could not parse age as years "{}"'.format(
                                        row["Import Key"], row["Aged"]
                                    )
                                )
                            )

                    if row["Died"]:
                        try:
                            dod = datetime.datetime.strptime(
                                row["Died"], "%d.%m.%Y"
                            ).date()
                            name.date_of_death = dod
                        except ValueError:
                            self.stdout.write(
                                self.style.WARNING(
                                    '{} Could not parse date of death "{}"'.format(
                                        row["Import Key"], row["Died"]
                                    )
                                )
                            )

                    if row["Born"]:
                        try:
                            dob = datetime.datetime.strptime(
                                row["Born"], "%d.%m.%Y"
                            ).date()
                            name.date_of_birth = dob
                        except ValueError:
                            self.stdout.write(
                                self.style.WARNING(
                                    '{} Could not parse date of birth "{}"'.format(
                                        row["Import Key"], row["Born"]
                                    )
                                )
                            )

                    name.save()

                    memorial.names.add(name)
                    memorial.save()

                except Location.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            "Unable to find location {}".format(row["Section"])
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Finished"))
