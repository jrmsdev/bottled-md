import bottle
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
        t = f(1468191315)
        self.assertEqual(t, 'Sun, 10 Jul 2016 19:55:15 -0300')
        t = f(1468191315, '%Y%m%d %H:%M:%S %z')
        self.assertEqual(t, '20160710 19:55:15 -0300')

    def test_static(self):
        f = bmd.static('bmd.css')
        self.assertIsInstance(f, bottle.HTTPResponse)
        self.assertEqual(f.status, '200 OK')
        self.assertEqual(f.content_type, 'text/css; charset=UTF-8')
        self.assertEqual(f.charset, 'UTF-8')
        self.assertEqual(len(f.body.read()), 561)

    def test_static404(self):
        with self.assertRaises(bottle.HTTPError) as cm:
            bmd.static('nonexistent.css')
        self.assertIsInstance(cm.exception, bottle.HTTPResponse)
        self.assertEqual(cm.exception.status, '404 Not Found')
        self.assertEqual(cm.exception.charset, 'UTF-8')
