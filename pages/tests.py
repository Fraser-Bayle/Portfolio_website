from django.test import TestCase, Client
from django.urls import reverse

class TestPagesViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_status_code(self):
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)

    def test_technologies_view_status_code(self):
        response = self.client.get(reverse('pages:technologies'))
        self.assertEqual(response.status_code, 200)

    def test_easter_egg_view_status_code(self):
        response = self.client.get(reverse('pages:easter_egg'))
        self.assertEqual(response.status_code, 200)

