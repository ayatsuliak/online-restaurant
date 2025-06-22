from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profile',
                                             email='test@u.com',
                                             password='pass123')
        self.client.login(username='profile', password='pass123')

    def test_update_profile_success(self):
        response = self.client.post(reverse('profile'), {
            'username': 'newusername',
            'email': 'newemail@example.com'
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')

    def test_update_duplicate_username(self):
        User.objects.create_user(username='taken',
                                 email='t@e.com',
                                 password='x')
        response = self.client.post(reverse('profile'), {
            'username': 'taken',
            'email': 'unique@example.com'
        })
        self.assertContains(response, "This username is already taken.")
