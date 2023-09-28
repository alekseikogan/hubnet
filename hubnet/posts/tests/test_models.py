from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание группы не более 15 символов',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def test_post_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expectedValue = post.text[:15]
        self.assertEquals(str(post), expectedValue)

    def test_group_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        expectedValue = group.title
        self.assertEquals(str(group), expectedValue)
