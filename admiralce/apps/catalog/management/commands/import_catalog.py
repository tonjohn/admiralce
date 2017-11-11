from django.core.management.base import BaseCommand
from django.utils.text import slugify
import csv
import re
from apps.users.models import User, Dog
from apps.sitters.models import Review, Sitter

USERID_REGEX = re.compile(r'user=(\d+)')


class Command(BaseCommand):
    help = 'Imports recovered review data'

    def handle(self, *args, **options):
        counter = 0
        print "Opening CSV..."
        with open('../reviews.csv') as f:
            is_header = True
            reader = csv.reader(f)
            """
                CSV format:
                0rating	1sitter_image	2end_date	3text	4owner_image
                5dogs	6sitter	7owner	8start_date
            """
            for row in reader:
                counter += 1
                if not is_header:
                    rating, sitter_image, end_date,\
                        review_text, owner_image, dogs,\
                        sitter, owner, start_date = row
                    # Sitter
                    user_id = USERID_REGEX.search(sitter_image).group(1)
                    fn = sitter[:len(sitter) - 3].strip()
                    ln = sitter[-2:].strip()
                    user_sitter, created = User.objects.get_or_create(
                        pk=user_id,
                        defaults={
                            'first_name': fn,
                            'last_name': ln,
                            'zipcode': 0,
                            'username': fn + ln + user_id,
                            'email': ""
                        }
                    )
                    if created:
                        # new sitter so we should create a profile for them
                        slug_fields = [user_id, fn, ln]
                        Sitter.objects.create(
                            user=user_sitter, url=slugify(
                                ' '.join(slug_fields)
                            )
                        )

                    # Owner
                    user_id = USERID_REGEX.search(owner_image).group(1)
                    fn = owner[:len(owner) - 3].strip()
                    ln = owner[-2:].strip()
                    user_owner, created = User.objects.get_or_create(
                        pk=user_id,
                        defaults={
                            'first_name': fn, 'last_name': ln,
                            'zipcode': 0,
                            'username': fn + ln + user_id,
                            'email': ""
                        }
                    )

                    # Dogs
                    for dog in dogs.split('|'):
                        new_dog, created = Dog.objects.get_or_create(
                            owner=user_owner, name=dog.strip()
                        )

                    # Review
                    review = Review(
                        review_text=review_text,
                        end_date=end_date,
                        start_date=start_date,
                        sitter=user_sitter,
                        owner=user_owner,
                        rating=rating
                    )
                    review.save()
                else:
                    print "Parsing rows..."
                    is_header = False

        # Finished import, now calculate scores
        print "Initial import complete. Calculating Sitter Rankings..."
        sitters = Sitter.objects.all()
        for sitter in sitters:
            sitter.user.calc_sitter_ranking
            sitter.save()
        self.stdout.write(
            self.style.SUCCESS('Successfully parsed %s records' % counter)
        )
