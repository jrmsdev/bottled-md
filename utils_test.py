import os
from os import path
from unittest import TestCase

import utils

class TestUtils(TestCase):

    def setUp(self):
        utils._G.scan_mode = False

    def chdir(self, dname):
        d = path.join(path.dirname(__file__), 'testdata', dname)
        os.chdir(d)

    def test_tpl_dict(self):
        d = utils.tpl_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d['timefmt'], utils.timefmt)
        self.assertEqual(d['url'], utils.url)
        self.assertEqual(d['static_url'], utils.static_url)

    def test_timefmt(self):
        t = utils.timefmt(1468191315)
        self.assertEqual(t, 'Sun, 10 Jul 2016 19:55:15 -0300')
        t = utils.timefmt(1468191315, '%Y%m%d %H:%M:%S %z')
        self.assertEqual(t, '20160710 19:55:15 -0300')

    def test_url(self):
        r = utils.url('fake/url')
        self.assertEqual(r, '/fake/url')

    def test_url_scan_mode(self):
        self.chdir('gendoc')
        utils.scan_mode('htdocs', 'htdocs/fake.md')
        r = utils.url('fake/url')
        self.assertEqual(r, 'fake/url')

    def test_url_scan_mode_dotted(self):
        self.chdir('gendoc')
        utils.scan_mode('htdocs', 'htdocs/s1/s2/s3/fake.md')
        r = utils.url('fake/url')
        self.assertEqual(r, '../../../fake/url')

    def test_static_url(self):
        r = utils.static_url('fake.url')
        self.assertEqual(r, '/static/fake.url')
