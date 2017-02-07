from unittest import mock

from django.test import TestCase

from core.managers.panda_manager import PandaManager, TransferFilter

TESTDATA_PATH = 'core/tests/assets'


class PandaManagerTest(TestCase):
    @mock.patch('core.managers.panda_manager.TRANSFERS_DIR', new=TESTDATA_PATH)
    def setUp(self):
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

    def test_filter_for_single_age(self):
        tf = TransferFilter(ages=[33])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Age == 33
        self.assertTrue(test_df.all())

    def test_filter_for_multiple_ages(self):
        tf = TransferFilter(ages=[32, 33])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Age.isin([32, 33])
        self.assertTrue(test_df.all())

    def test_filter_for_single_strength(self):
        tf = TransferFilter(strengths=[17])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Strength == 17
        self.assertTrue(test_df.all())

    def test_filter_for_multiple_strengths(self):
        tf = TransferFilter(strengths=[17, 18])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Strength.isin([17, 18])
        self.assertTrue(test_df.all())

    def test_filter_for_single_season(self):
        tf = TransferFilter(seasons=[146])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Season == 146
        self.assertTrue(test_df.all())

    def test_filter_for_single_matchday(self):
        tf = TransferFilter(matchdays=[0])
        df = self.panda_manager.filter_transfers(tf)
        test_df = df.Matchday == 0
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
