from unittest import TestCase

import bmd

class TestBMD(TestCase):

    @bmd.tpl_utils
    def fakeview(self):
        return dict()

    def test_tpl_utils(self):
        d = self.fakeview()
        self.assertIsInstance(d, dict)

    def test_tpl_utils_timefmt(self):
        f = self.fakeview().get('timefmt')
        t = f('%Y%m%d %H:%M:%S %z', 1468191315)
        self.assertEqual(t, '20160710 19:55:15 -0300')
