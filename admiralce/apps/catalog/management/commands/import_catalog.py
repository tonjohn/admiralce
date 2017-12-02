from django.core.management.base import BaseCommand
from django.utils.text import slugify
import csv
import re
from apps.users.models import User
from apps.catalog.models import Provider, Course

USERID_REGEX = re.compile(r'user=(\d+)')


class Command(BaseCommand):
    help = 'Imports data from scraper'

    def handle(self, *args, **options):
        counter = 0
        print "Opening CSV..."
        with open('ada.csv') as f:
            is_header = True
            reader = csv.reader(f)
            """
                CSV format:
                    0) Title
                    1) Subject
                    2) Dates
                    3) Location
                    4) Cost
                    5) Provider
                    6) Type
                    7) Description
                    8) Website
            """
            for row in reader:
                counter += 1
                if not is_header:
                    title, subject, dates,\
                        location, cost_string, provider_name,\
                        event_type, description, provider_url, test = row
                    # Provider
                    obj_provider, created = Provider.objects.get_or_create(
                        name=provider_name,
                        defaults={
                            'name': provider_name,
                            'base_url': provider_url,
                        }
                    )

                    cost_string = cost_string.strip()
                    cost = 0.00
                    if len(cost_string) > 0:
                        cost = float(cost_string.split(' ', 1)[0])
                    print "COST: ",'%.2f' % cost

                    # Course
                    new_course = Course(
                        provider=obj_provider,
                        name=title,
                        description=description,
                        credits=0,
                        fee=cost,
                        is_online=False,
                    )
                    new_course.save()
                else:
                    print "Parsing rows..."
                    is_header = False

        # Finished import, now calculate scores
        print "Initial import complete."
        self.stdout.write(
            self.style.SUCCESS('Successfully parsed %s records' % counter)
        )
