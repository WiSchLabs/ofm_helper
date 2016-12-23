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
        matching_users = OFMUser.objects.filter(username='new')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertEqual(matching_users.count(), 1)
        self.assertNotEqual(matching_users[0].password, '1234')
        self.assertEqual(matching_users[0].email, 'new@ofmhelper.com')
        self.assertEqual(matching_users[0].ofm_username, 'abc')
        self.assertEqual(matching_users[0].ofm_password, 'def')

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
                                    {'username': 'unmatch_pw', 'password': '1234', 'password2': '12345',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertEqual(OFMUser.objects.filter(username='unmatch_pw').count(), 0)

    def test_register_with_unmatching_ofm_passwords(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'unmatch_ofm_pw', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'abc', 'ofm_password': 'def', 'ofm_password2': 'ghj'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertEqual(OFMUser.objects.filter(username='unmatch_ofm_pw').count(), 0)

    def test_register_with_already_registered_ofm_username(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'ofm_user_already_registered', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'ofm', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertEqual(OFMUser.objects.filter(username='ofm_user_already_registered').count(), 0)

    def test_register_with_already_registered_email(self):
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'email_already_registered', 'password': '1234', 'password2': '1234',
                                     'email': 'temporary@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/register.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated())
        self.assertEqual(OFMUser.objects.filter(username='email_already_registered').count(), 0)

    def test_register_when_already_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:account:register'),
                                    {'username': 'user_already_logged_in', 'password': '1234', 'password2': '1234',
                                     'email': 'new@ofmhelper.com',
                                     'ofm_username': 'new', 'ofm_password': 'def', 'ofm_password2': 'def'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.assertEqual(OFMUser.objects.filter(username='user_already_logged_in').count(), 0)
