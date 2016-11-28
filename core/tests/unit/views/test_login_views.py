from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import OFMUser


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user('temporary', 'temporary@ofmhelper.com', 'temporary')

    def test_login_redirects_for_unknown_user(self):
        response = self.client.post(reverse('core:login'), {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('core:login'), {'username': 'temporary', 'password': 'temporary'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('core:login'), {'username': 'temporary', 'password': 'incorrect'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_login_already_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:login'), {'username': 'temporary', 'password': 'temporary'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_with_inactive_account(self):
        OFMUser.objects.create_user('disabled', 'diasabled@gmail.com', 'disabled', is_active=False)
        response = self.client.post(reverse('core:login'), {'username': 'disabled', 'password': 'disabled'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_call_login_page_when_already_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_logout_when_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_logout_when_not_logged_in(self):
        response = self.client.get(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_view_account_when_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_view_account_when_not_logged_in(self):
        response = self.client.get(reverse('core:account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())
