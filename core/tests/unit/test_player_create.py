from django.test import TestCase

from core.factories.core_factories import PlayerFactory


class CreatePlayerTest(TestCase):
    def test_create_player(self):
        p = PlayerFactory.create(position=1, name='tw1', nationality='Deutschland')
        self.assertIsNotNone(p)
        self.assertEquals(p.position, 1)
        self.assertEquals(p.name, 'tw1')
        self.assertEquals(p.nationality, 'Deutschland')
        self.assertEquals(p.birthSeason.number, 1)
