from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import OFMUser


class RegistrationTestCase(TestCase):
    def setUp(self):
        OFMUser.objects.create_user(
            username='temporary',
            email='temporary@ofmhelper.com',
            password='temporary',
            ofm_username='ofm',
            ofm_password='ofm'
        )

    def test_register_new_account(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_existing_username(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'temporary', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_unmatching_passwords(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '12345',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_unmatching_ofm_passwords(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'ghj'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_already_registered_ofm_username(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'ofm', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_with_already_registered_email(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'temporary@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_register_when_already_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'new', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
