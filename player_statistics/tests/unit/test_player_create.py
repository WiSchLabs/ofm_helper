import unittest

from player_statistics.factories.player_factories import PlayerFactory


class CreatePlayerTest(unittest.TestCase):
    def test_create_player(self):
        p = PlayerFactory.create(position=1, name='tw1', nationality='Deutschland')
        self.assertIsNotNone(p)
        self.assertEquals(p.position, 1)
        self.assertEquals(p.name, 'tw1')
        self.assertEquals(p.nationality, 'Deutschland')
        self.assertEquals(p.birth.season, 1)
        self.assertEquals(p.age, 17)
        self.assertEquals(p.matchday.matchday, 1)


if __name__ == '__main__':
    unittest.main()
