from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostApiTests(APITestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username="blogger",
        )
        self.post = Post.objects.create(
            title="First post",
            slug="first-post",
            body="Post body",
            author=self.author,
        )

    def test_list_posts_includes_author_name(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], self.post.title)
        self.assertEqual(response.data[0]["author_name"], self.author.username)

    def test_create_post(self):
        response = self.client.post(
            reverse("post-list"),
            {
                "title": "Another post",
                "slug": "another-post",
                "body": "More writing",
                "status": Post.Status.PUBLISHED,
                "author": self.author.pk,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.author.pk)
        self.assertTrue(
            Post.objects.filter(slug="another-post", author=self.author).exists()
        )

    def test_update_post(self):
        response = self.client.patch(
            reverse("post-detail", args=[self.post.pk]),
            {"title": "Updated title"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated title")

    def test_delete_post(self):
        response = self.client.delete(reverse("post-detail", args=[self.post.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
