from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_post(self):
        response = self.client.post('/api/posts/', {
            'text': 'Test Post',
            'image': 'path_to_image.jpg'  # Замените на реальный путь к изображению
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment(self):
        post = Post.objects.create(author=self.user, text='Post for comment', image='path_to_image.jpg')
        response = self.client.post('/api/comments/', {
            'post': post.id,
            'text': 'Test Comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
