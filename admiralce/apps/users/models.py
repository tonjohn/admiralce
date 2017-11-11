from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Dog(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="dogs")
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
    def calc_sitter_ranking(self):
        review_count = self.reviews_received.count()
        # print "Review Count", review_count

        sitter_ranking = self.calc_sitter_score()
        # print "Sitter Score", sitter_ranking

        if review_count > 0:
            ratings_score = self.calc_ratings_score()
            if review_count >= 10:
                sitter_ranking = ratings_score
            else:
                # print "Is this thing on?"
                pct_stays = review_count / 10.00
                # print "pct_stays", pct_stays
                weighted_sitter_score = sitter_ranking * (1 - pct_stays)
                # print "weighted sitter score", weighted_sitter_score
                weighted_ratings_score = ratings_score * pct_stays
                # print "weighted ratings score", weighted_ratings_score
                sitter_ranking = weighted_ratings_score + weighted_sitter_score

        self.sitter_profile.rank = sitter_ranking
        # print "Sitter Ranking", sitter_ranking
        return sitter_ranking
