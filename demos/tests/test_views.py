from django.test import TestCase, Client
from django.urls import reverse

class TestDemoViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_demo_view_status_code(self):
        response = self.client.get(reverse('demos:demo_index'))
        self.assertEqual(response.status_code, 200)

# TODO: Other tests