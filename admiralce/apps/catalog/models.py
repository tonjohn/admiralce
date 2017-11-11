from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class CourseManager(models.Manager):
    def add_course(self, provider, name, credits, fee, url, speaker, zip, is_online):
        review, created = self.get_or_create(provider=provider, name=name,
                                             defaults={'credits': credits,
                                                       'fee': fee,
                                                       'url': url,
                                                       'speaker':
                                                           speaker,
                                                       'zipcode': zip,
                                                       'is_online': is_online,
                                                       }
                                             )

        return created

    def del_course(self, cid):
        # fetch the review so we can find the sitter
        course = self.get(id=cid)

        return course.delete()  # delete the review

'''
    Provider of Continuing Education courses.
'''


class Provider(models.Model):
    name = models.CharField(max_length=255, blank=True)
    base_url = models.URLField(blank=True)
    # catalog_urls = csv or another table?
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


'''
    Continuing Education Course catalog
'''


class Course(models.Model):
    provider = models.ForeignKey('Provider', related_name="catalog")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    credits = models.FloatField(
        default=0, blank=True
    )
    fee = models.FloatField(
        default=0, blank=True
    )
    url = models.URLField(blank=True, null=True)
    speaker = models.CharField(max_length=255, blank=True)  # TODO: make speakers a FK
    zipcode = models.IntegerField(blank=True, null=True)  # should be blank if Online Only maybe?
    is_online = models.BooleanField(blank=True)  # Is the course available online?
    # address
    # start time
    # end time
    # duration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CourseManager()
