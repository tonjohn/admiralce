from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class ReviewManager(models.Manager):
    def add_review(self, owner, sitter, start, end, rating, review_text):
        review, created = self.get_or_create(owner=owner, sitter=sitter,
                                             defaults={'start_date': start,
                                                       'end_date': end,
                                                       'rating': rating,
                                                       'review_text':
                                                           review_text}
                                             )

        if created:
            sitter.calc_sitter_ranking
            sitter.sitter_profile.save()

        return created

    def del_review(self, id):
        # fetch the review so we can find the sitter
        review = self.get(id=id)
        sitter = review.sitter

        review.delete()  # delete the review

        # recalculate sitter ranking and save to db
        sitter.calc_sitter_ranking
        sitter.sitter_profile.save()

        return True


class Sitter(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="sitter_profile"
    )
    title = models.CharField(max_length=255, blank=True)
    url = models.SlugField(blank=True)
    rank = models.FloatField(
        default=0, blank=True
    )
    ratings_score = models.FloatField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    rating = models.IntegerField()
    sitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reviews_received"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reviews_given"
    )
    review_text = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    class Meta:
        ordering = ['-end_date']


class PetService(models.Model):
    name = models.TextField()
