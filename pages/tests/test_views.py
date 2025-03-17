from django.test import TestCase, Client
from django.urls import reverse

class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_homepage_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_homepage_contains_correct_html(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'html')

    def test_homepage_does_not_contain_incorrect_html(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Hi there! I should not be on the page.')