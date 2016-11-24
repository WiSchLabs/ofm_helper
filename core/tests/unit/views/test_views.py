from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import OFMUser


class LoginTestCase(TestCase):
    def setUp(self):
        OFMUser.objects.create_user('temporary', 'temporary@ofmhelper.com', 'temporary')

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

    def test_view_account_settings_when_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_view_account_settings_when_not_logged_in(self):
        response = self.client.get(reverse('core:settings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())


class RegistrationTestCase(TestCase):
    def setUp(self):
        OFMUser.objects.create_user('temporary', 'temporary@ofmhelper.com', 'temporary', ofm_username='ofm',
                                    ofm_password='ofm')

    def test_register_new_account(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_existing_username(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'temporary', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:register'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_unmatching_passwords(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '12345',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:register'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_unmatching_ofm_passwords(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'ghj'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:register'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_already_registered_ofm_username(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'ofm', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:register'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_already_registered_email(self):
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'temporary@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:register'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_when_already_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
