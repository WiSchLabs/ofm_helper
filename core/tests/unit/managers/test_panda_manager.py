from unittest.mock import patch

from django.test import TestCase

from core.managers.panda_manager import PandaManager, TransferFilter

TESTDATA_PATH = 'core/tests/assets'


class PandaManagerTest(TestCase):
    @patch('core.managers.panda_manager')
    def setUp(self, panda_manager_mock):
        panda_manager_mock = PandaManager
        panda_manager_mock.transfers_dir = TESTDATA_PATH

        self.panda_manager = PandaManager()

    def test_loading(self):

        self.assertIsNotNone(self.panda_manager)
        self.assertIsNotNone(self.panda_manager.data_frame)

        self.assertIsNotNone(self.panda_manager.data_frame.Position)
        self.assertIsNotNone(self.panda_manager.data_frame.Age)
        self.assertIsNotNone(self.panda_manager.data_frame.Strength)
        self.assertIsNotNone(self.panda_manager.data_frame.Price)
        self.assertIsNotNone(self.panda_manager.data_frame.Season)
        self.assertIsNotNone(self.panda_manager.data_frame.Matchday)

    def test_filter_for_nothing(self):
        df = self.panda_manager.filter_transfers()
        self.assertEqual(len(df), len(self.panda_manager.data_frame))

    def test_filter_for_single_position(self):
        tf = TransferFilter(positions=['MS'])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Position == 'MS'
        self.assertTrue(test_df.all())

    def test_filter_for_multiple_positions(self):
        tf = TransferFilter(positions=['MS', 'TW'])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Position.isin(['MS', 'TW'])
        self.assertTrue(test_df.all())

    def test_filter_for_min_price(self):
        min_price = 100000
        tf = TransferFilter(min_price=min_price)
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Price >= min_price
        self.assertTrue(test_df.all())

    def test_filter_for_max_price(self):
        max_price = 10000000
        tf = TransferFilter(max_price=max_price)
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Price <= max_price
        self.assertTrue(test_df.all())
