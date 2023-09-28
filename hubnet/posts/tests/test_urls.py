from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus
from hubnet.posts.tests.test_models import PostModelTest

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_user = User.objects.create_user(username='Guest')
        cls.authorized = User.objects.create_user(username='Authorized')
        cls.author_user = User.objects.create_user(username='Author_post')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы не более 15 символов'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized)
        self.author_client = Client()
        self.author_client.force_login(self.author_user)

    def test_public_urls_guest(self):
        """Проверка доступности общих страниц для гостя"""
        post_id = PostURLTests.post.id

        url_names = [
            '/',
            '/group/test-slug/',
            '/profile/Author_post/',
            f'/posts/{post_id}/'
        ]
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200)

    def test_post_edit_for_guest(self):
        """Страница posts/<int:post_id>/edit/ перенаправляет гостя на вход"""
        post_id = PostModelTest.post.id
        responce = self.guest_client.get(
             f'/posts/{post_id}/edit/', follow=True)
        self.assertRedirects(
            responce, f'auth/login/?next=/posts/{post_id}/edit/')
