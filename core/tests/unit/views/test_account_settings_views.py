from django.core.urlresolvers import reverse
from django.test import TestCase

from users.models import OFMUser


class AccountSettingsTestCase(TestCase):
    def setUp(self):
        self.user = OFMUser.objects.create_user(
            username='temporary',
            email='temporary@ofmhelper.com',
            password='temporary',
            ofm_username="tmp",
            ofm_password="temp"
        )

    def test_view_account_settings_when_logged_in(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('core:account:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_view_account_settings_when_not_logged_in(self):
        response = self.client.get(reverse('core:account:settings'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

    def test_change_email(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:account:settings'), {'email': 'new@mail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.assertEqual(response.wsgi_request.user.email, 'new@mail.com')

    def test_change_password(self):
        OFMUser.objects.create_user('second', 'second@ofmhelper.com', 'second')
        self.client.login(username='second', password='second')
        response = self.client.post(reverse('core:account:settings'),
                                    {'password': 'Zillertal', 'password2': 'Zillertal'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.client.get(reverse('core:account:logout'))

        response = self.client.post(reverse('core:account:login'), {'username': 'second', 'password': 'second'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

        response = self.client.post(reverse('core:account:login'), {'username': 'second', 'password': 'Zillertal'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_change_ofm_password(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:account:settings'),
                                    {'ofm_password': 'Zillertal', 'ofm_password2': 'Zillertal'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.assertEqual(response.wsgi_request.user.ofm_password, 'Zillertal')

    def test_change_ofm_password_when_unmatching(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(reverse('core:account:settings'),
                                    {'ofm_password': 'Zillertal', 'ofm_password2': 'Berlin'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.assertEqual(response.wsgi_request.user.ofm_password, 'temp')

    def test_change_password_when_unmatching(self):
        OFMUser.objects.create_user('third', 'third@ofmhelper.com', 'third')
        self.client.login(username='third', password='third')
        response = self.client.post(reverse('core:account:settings'), {'password': 'Zillertal', 'password2': 'Berlin'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/settings.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
        self.client.get(reverse('core:account:logout'))

        response = self.client.post(reverse('core:account:login'), {'username': 'third', 'password': 'Zillertal'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated())

        response = self.client.post(reverse('core:account:login'), {'username': 'third', 'password': 'third'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/account/home.html')
        self.assertTrue(response.wsgi_request.user.is_authenticated())
