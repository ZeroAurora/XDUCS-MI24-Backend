from django.test import TestCase
from django.contrib.auth.models import User
from user.models import Profile, FollowRelationship
from django.core.files.uploadedfile import SimpleUploadedFile


from file.models import MediaFile


class ProfileModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.media_file = MediaFile.objects.create(
            file=SimpleUploadedFile(name="test_image.jpg", content=b"file_content", content_type="image/jpeg"),
            owner=cls.user,
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            bio="Test bio",
            profile_picture=self.media_file,
            date_of_birth="2000-01-01",
            location="Test Location",
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, "Test bio")
        self.assertEqual(profile.profile_picture, self.media_file)
        self.assertEqual(str(profile.date_of_birth), "2000-01-01")
        self.assertEqual(profile.location, "Test Location")

    def test_optional_fields(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.bio, "")
        self.assertIsNone(profile.profile_picture)
        self.assertIsNone(profile.date_of_birth)
        self.assertEqual(profile.location, "")

    def test_profile_str_representation(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), self.user.username)


class FollowerModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="testpass123")
        cls.user2 = User.objects.create_user(username="user2", password="testpass123")

    def test_follower_creation(self):
        follower = FollowRelationship.objects.create(follower=self.user1, followed=self.user2)
        self.assertEqual(follower.follower, self.user1)
        self.assertEqual(follower.followed, self.user2)
        self.assertIsNotNone(follower.created_at)

    def test_unique_follower_followed_constraint(self):
        FollowRelationship.objects.create(follower=self.user1, followed=self.user2)
        with self.assertRaises(Exception):
            FollowRelationship.objects.create(follower=self.user1, followed=self.user2)

    def test_follower_str_representation(self):
        follower = FollowRelationship.objects.create(follower=self.user1, followed=self.user2)
        expected_str = f"{self.user1.username} follows {self.user2.username}"
        self.assertEqual(str(follower), expected_str)
