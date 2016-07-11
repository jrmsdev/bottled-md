import os
import bottle
from os import path
from unittest import TestCase

import bmd

class TestBMD(TestCase):

    @bmd.tpl_utils
    def fakeview(self):
        return dict()

    def chdir(self, dname):
        d = path.join(path.dirname(__file__), 'testdata', dname)
        os.chdir(d)

    def test_tpl_utils(self):
        d = self.fakeview()
        self.assertIsInstance(d, dict)

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

    def test_gendoc(self):
        self.chdir('gendoc')
        d = bmd.gendoc('index.md')
        self.assertIsInstance(d, str)
        self.assertEqual(len(d), 373)

    def test_gendoc404(self):
        self.chdir('gendoc')
        with self.assertRaises(bottle.HTTPError) as cm:
            bmd.gendoc('nonexistent.md')
        r = cm.exception
        self.assertIsInstance(r, bottle.HTTPResponse)
        self.assertEqual(r.status, '404 Not Found')
