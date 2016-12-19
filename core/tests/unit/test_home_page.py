from django.test import TestCase


class HomePageTest(TestCase):
    def test_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get('/account/register')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 200)

    def test_account_page(self):
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 301)
