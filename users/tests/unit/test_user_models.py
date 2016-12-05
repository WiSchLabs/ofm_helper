from django.test import TestCase

from users.models import OFMUser


class CreateOFMUserModelsTest(TestCase):
    def test_create_season(self):
        u = OFMUser(username='test', password='1234')
        self.assertIsNotNone(u)
        self.assertEqual(u.username, 'test')
        self.assertEqual(u.password, '1234')
