from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Post, Comment, Like
from django.core.files.uploadedfile import SimpleUploadedFile
from file.models import MediaFile


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.user2 = User.objects.create_user(username="testuser2", password="testpass123")

    def test_post_creation(self):
        post = Post.objects.create(user=self.user, content="Test post content")
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.content, "Test post content")
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_post_str_representation(self):
        post = Post.objects.create(user=self.user, content="Test post")
        expected_str = f"Post by {self.user.username} at {post.created_at}"
        self.assertEqual(str(post), expected_str)

    def test_multiple_users_interacting(self):
        post = Post.objects.create(user=self.user, content="Test post")
        # User2 likes the post
        Like.objects.create(user=self.user2, post=post)
        # User2 comments on the post
        comment = Comment.objects.create(user=self.user2, post=post, content="Nice post!")
        # User replies to the comment
        reply = Comment.objects.create(user=self.user, post=post, content="Thanks!", parent=comment)

        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(post.comments.count(), 2)
        self.assertEqual(comment.replies.count(), 1)
        self.assertEqual(reply.parent, comment)

    def test_post_update(self):
        post = Post.objects.create(user=self.user, content="Initial content")
        post.content = "Updated content"
        post.save()

        updated_post = Post.objects.get(id=post.id)
        self.assertEqual(updated_post.content, "Updated content")
        self.assertNotEqual(updated_post.created_at, updated_post.updated_at)


class PostMediaFilesModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.post = Post.objects.create(user=cls.user, content="Test post")
        cls.media_file = MediaFile.objects.create(
            file=SimpleUploadedFile(name="test_image.jpg", content=b"file_content", content_type="image/jpeg"),
            owner=cls.user,
        )

    def test_post_media_files_relationship(self):
        # Add media file to post
        self.post.media_files.add(self.media_file)

        # Verify the relationship
        self.assertEqual(self.post.media_files.count(), 1)
        self.assertEqual(self.post.media_files.first(), self.media_file)
        self.assertEqual(self.media_file.owner, self.user)

    def test_multiple_media_files(self):
        # Create additional media file
        media_file2 = MediaFile.objects.create(
            file=SimpleUploadedFile(name="test_image2.jpg", content=b"file_content", content_type="image/jpeg"),
            owner=self.user,
        )

        # Add both media files to post
        self.post.media_files.add(self.media_file, media_file2)

        # Verify both files are associated
        self.assertEqual(self.post.media_files.count(), 2)
        self.assertIn(self.media_file, self.post.media_files.all())
        self.assertIn(media_file2, self.post.media_files.all())


class CommentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.user2 = User.objects.create_user(username="testuser2", password="testpass123")
        cls.post = Post.objects.create(user=cls.user, content="Test post")

    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user, post=self.post, content="Test comment")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.content, "Test comment")
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)

    def test_comment_str_representation(self):
        comment = Comment.objects.create(user=self.user, post=self.post, content="Test comment")
        expected_str = f"Comment by {self.user.username} on {self.post}"
        self.assertEqual(str(comment), expected_str)

    def test_nested_comments(self):
        parent_comment = Comment.objects.create(user=self.user, post=self.post, content="Parent comment")
        child_comment = Comment.objects.create(
            user=self.user2, post=self.post, content="Child comment", parent=parent_comment
        )

        self.assertEqual(parent_comment.replies.count(), 1)
        self.assertEqual(child_comment.parent, parent_comment)
        self.assertEqual(self.post.comments.count(), 2)


class LikeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.user2 = User.objects.create_user(username="testuser2", password="testpass123")
        cls.post = Post.objects.create(user=cls.user, content="Test post")

    def test_like_creation(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertIsNotNone(like.created_at)

    def test_unique_user_post_constraint(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, post=self.post)

    def test_like_str_representation(self):
        like = Like.objects.create(user=self.user, post=self.post)
        expected_str = f"Like by {self.user.username} on {self.post}"
        self.assertEqual(str(like), expected_str)

    def test_multiple_likes_from_different_users(self):
        Like.objects.create(user=self.user, post=self.post)
        Like.objects.create(user=self.user2, post=self.post)
        self.assertEqual(self.post.likes.count(), 2)
        self.assertEqual(self.post.likes.filter(user=self.user).count(), 1)
        self.assertEqual(self.post.likes.filter(user=self.user2).count(), 1)
