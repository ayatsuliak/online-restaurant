from django.test import TestCase
from django.urls import reverse

from menu.models import MenuItem


class MenuViewTests(TestCase):
    def setUp(self):
        self.item = MenuItem.objects.create(name='Sushi', price=200)

    def test_menu_list_view(self):
        response = self.client.get(reverse('menu:menu_list'))
        self.assertContains(response, 'Sushi')

    def test_menu_detail_view(self):
        response = self.client.get(reverse('menu:item_detail',
                                           kwargs={'pk': self.item.pk}))
        self.assertContains(response, 'Sushi')
