from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthTests(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_user(self):
        User.objects.create_user(username='loginuser', password='pass1234')

        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/'))

    def test_logout(self):
        self.client.login(username='logoutuser', password='pass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
