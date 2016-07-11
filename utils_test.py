from os import path
from unittest import TestCase

import utils

class TestUtils(TestCase):

    def test_utils_timefmt(self):
        t = utils.timefmt(1468191315)
        self.assertEqual(t, 'Sun, 10 Jul 2016 19:55:15 -0300')
        t = utils.timefmt(1468191315, '%Y%m%d %H:%M:%S %z')
        self.assertEqual(t, '20160710 19:55:15 -0300')
