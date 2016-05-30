import unittest

from player_statistics.models import Player


class CreatePlayerTest(unittest.TestCase):
    def test_create_player(self):
        p = Player(position=1, name='tw1', nationality='Deutschland')
        self.assertIsNotNone(p)
        self.assertEquals(p.position, 1)
        self.assertEquals(p.name, 'tw1')
        self.assertEquals(p.nationality, 'Deutschland')


if __name__ == '__main__':
    unittest.main()
