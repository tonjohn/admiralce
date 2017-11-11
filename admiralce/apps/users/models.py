from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class PracticeAddress(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="practices")
    # breed = models.ForeignKey(Breed)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    zipcode = models.IntegerField(blank=True, null=True)

    """
        Ratings Score is the average of their stay ratings.
    """

    def calc_ratings_score(self):
        from django.db.models import Avg
        score = self.reviews_received.aggregate(Avg('rating')).values()[0]
        # print "AVG", score
        self.sitter_profile.ratings_score = score

        return score

    """
        Sitter Score is 5 times the fraction of the English alphabet
        comprised by the distinct letters in
            what we've recovered of the sitter's name.
    """

    def calc_sitter_score(self):
        name = self.first_name.lower() + self.last_name.lower()
        unique_char = len(set(''.join(filter(unicode.isalpha, name))))
        score = 5.00 * (unique_char / 26.00)
        return score

    """
        The Overall Sitter Rank is a weighted average of the Sitter Score
            and Ratings Score, weighted by the number of stays.
        When a sitter has no stays,
            their Overall Sitter Rank is equal to the Sitter Score.
        When a sitter has 10 or more stays,
            their Overall Sitter Rank is equal to the Ratings Score.
    """

    @property
    def current_credits(self):
        # review_count = self.reviews_received.count()
        # print "Review Count", review_count

        # print "Sitter Ranking", sitter_ranking
        return 10
