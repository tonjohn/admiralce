from django.utils import timezone
from django.test import TestCase
from django.utils.text import slugify

from .models import Provider, Course
from ..users.models import User


class ReviewTest(TestCase):
    users = []
    providers = [
        Provider.objects.create(
            username="tonjohn",
            email="a@a.a",
            first_name="Qwertyuiopas",
            last_name="J.",
            zipcode=98034
        ),
    ]
    courses = []

    def setUp(self):
        # Create some test users
        self.users = [
            User.objects.create(
                username="tonjohn",
                email="a@a.a",
                first_name="Qwertyuiopas",
                last_name="J.",
                zipcode=98034
            ),
            User.objects.create(
                username="asira",
                email="b@b.b",
                first_name="Arisa",
                last_name="S.",
                zipcode=98004
            ),
            User.objects.create(
                username="bujo",
                email="c@b.b",
                first_name="Hubert",
                last_name="C.",
                zipcode=98004
            ),
            User.objects.create(
                username="ronnie",
                email="d@b.b",
                first_name="Twee",
                last_name="N.",
                zipcode=98004
            ),
            User.objects.create(
                username="timbob",
                email="e@b.b",
                first_name="Zach",
                last_name="E.",
                zipcode=98004
            ),
            User.objects.create(
                username="chewygranola",
                email="f@b.b",
                first_name="Abdul",
                last_name="I.",
                zipcode=98004),
            User.objects.create(
                username="utredsonofutred",
                email="g@b.b",
                first_name="Rober",
                last_name="K.",
                zipcode=98004
            ),
        ]

        # Create test sitter profiles
        title = "Fun times ahead!"
        for user in self.users:
            slug_fields = [user.first_name, user.last_name[:1], title]
            Sitter.objects.create(
                title=title, url=slugify(' '.join(slug_fields)), user=user
            )

    # Tests adding a review via the ReviewManager
    def test_add_new_review(self):
        owner = User.objects.get(id=1)
        sitter = User.objects.get(id=2)

        self.assertEqual(
            Review.objects.add_review(
                owner, sitter, timezone.now(), timezone.now(), 5,
                "My dog cheyenne had a great time!"
            ), True
        )

    def test_review_score_5_reviews(self):

        sitter = User.objects.get(id=1)

        for i in xrange(1, 6):
            owner = self.users[i]
            Review.objects.add_review(
                owner, sitter, timezone.now(), timezone.now(), 5,
                "My dog cheyenne had a great time!"
            )

        self.assertEqual(sitter.sitter_profile.rank, 3.75)

    # Test deleting review through ReviewManager
    def test_delete_review(self):
        sitter = User.objects.get(id=1)
        for i in xrange(1, 6):
            owner = self.users[i]
            Review.objects.add_review(
                owner, sitter, timezone.now(), timezone.now(), 5,
                "My dog cheyenne had a great time!"
            )

        review = sitter.reviews_received.last()

        Review.objects.del_review(review.id)  # delete the review
        # need to refresh the user to get the new score
        sitter = User.objects.get(id=1)

        self.assertEqual(sitter.sitter_profile.rank, 3.5)
