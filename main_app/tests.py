from django.test import TestCase
from django.urls import reverse
from .models import User, Notation, UserProfile, Friendship
from .forms import SignUpForm, NotationForm, UserProfileForm

class UserTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login(self):
        # Тестирование процесса входа в систему
        response = self.client.post('/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)

    def test_sign_up(self):
        # Тестирование процесса регистрации
        form_data = {'username': 'newuser', 'password1': '12345', 'password2': '12345'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_get_profile(self):
        # Тестирование получения профиля пользователя
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('notion:get_profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

class NotationTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя и заметку для тестирования
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.notation = Notation.objects.create(author=self.user, content='Test Notation', is_public=True)

    def test_get_notation(self):
        # Тестирование получения заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('notion:get_notion', args=[self.notation.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_notation(self):
        # Тестирование обновления заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notion:update_notion', args=[self.notation.id]), {'content': 'Updated'})
        self.notation.refresh_from_db()
        self.assertEqual(self.notation.content, 'Updated')

    def test_delete_notation(self):
        # Тестирование удаления заметки
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('notion:delete_notion', args=[self.notation.id]))
        self.assertEqual(response.status_code, 302)  # Перенаправление после удаления


class UserProfileTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя с профилем для тестирования
        self.user = User.objects.create_user(username='user', password='12345')
        self.userprofile = UserProfile.objects.create(user=self.user)

    def test_update_profile_pic(self):
        # Тестирование обновления изображения профиля
        self.client.login(username='user', password='12345')
        with open('path/to/your/image.jpg', 'rb') as file:
            response = self.client.post(reverse('notion:update_profile_pic'), {'profile_pic': file}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.userprofile.refresh_from_db()
        self.assertTrue(self.userprofile.profile_pic)  # Проверка, что изображение обновлено
