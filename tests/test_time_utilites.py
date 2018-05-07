import unittest

from time_utilites import time_diff


class TestTimeUtility(unittest.TestCase):
    def test_time_diff_zero(self):
        diff = time_diff('00:00:00', '00:00:00')
        self.assertEqual(0, diff)

    def test_time_diff_st_gt_et(self):
        diff = time_diff('00:01:00', '00:2:00')
        self.assertEqual(60, diff)

    def test_time_diff_st_lt_et(self):
        diff = time_diff('00:01:00', '00:2:00')
        self.assertEqual(60, diff)
