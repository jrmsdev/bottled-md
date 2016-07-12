import os
import bottle
from os import path
from unittest import TestCase

import bmd
import utils

class TestBMD(TestCase):

    def setUp(self):
        utils._G.scan_mode = False

    @bmd.tpl_utils
    def fakeview(self):
        return dict()

    def dirpath(self, dname):
        return path.join(path.dirname(__file__), 'testdata', dname)

    def chdir(self, dname):
        os.chdir(self.dirpath(dname))

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
        f.body.close()

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

    def test_index(self):
        self.chdir('gendoc')
        d = bmd.index()
        self.assertIsInstance(d, str)
        self.assertEqual(len(d), 373)

    def test_index_readme(self):
        self.chdir('gendoc-readme')
        d = bmd.index()
        self.assertIsInstance(d, str)
        self.assertEqual(len(d), 375)

    def test_noindex(self):
        self.chdir('gendoc-noindex')
        with self.assertRaises(bottle.HTTPError) as cm:
            bmd.index()
        r = cm.exception
        self.assertIsInstance(r, bottle.HTTPResponse)
        self.assertEqual(r.status, '404 Not Found')

    def test_sync_static(self):
        srcdir = self.dirpath('sync-static')
        src_f = path.join(srcdir, 'file.txt')
        dstdir = self.dirpath('sync-static.out')
        dst_f = path.join(dstdir, 'file.txt')
        bmd.sync_static(srcdir, dstdir)
        src_fh = open(src_f, 'r')
        dst_fh = open(dst_f, 'r')
        self.assertEqual(src_fh.read(), dst_fh.read())
        src_fh.close()
        dst_fh.close()
        os.unlink(dst_f)
        os.rmdir(dstdir)

    def test_sync_static_nosrc(self):
        with self.assertRaises(FileNotFoundError):
            bmd.sync_static(self.dirpath('sync-static.nonexistent'),
                                        self.dirpath('sync-static.out'))

    def test_sync_static_dsterror(self):
        srcdir = self.dirpath('sync-static')
        dstdir = '/nonexistent'
        with self.assertRaises(PermissionError):
            bmd.sync_static(srcdir, dstdir)

    def rmdir_scanout(self):
        dstdir = self.dirpath('scan.out')
        for n in ('static/bmd.css', 'index.html'):
            f = path.join(dstdir, n)
            os.unlink(f)
        for n in ('static', ''):
            d = path.join(dstdir, n)
            os.rmdir(d)

    def test_scan(self):
        srcdir = self.dirpath('gendoc')
        dstdir = self.dirpath('scan.out')
        r = bmd.scan(srcdir, dstdir)
        self.assertEqual(r, 0)
        self.rmdir_scanout()

    def test_scan_out_exists(self):
        srcdir = self.dirpath('gendoc')
        dstdir = self.dirpath('scan.out')
        os.makedirs(dstdir)
        r = bmd.scan(srcdir, dstdir)
        self.assertEqual(r, 0)
        self.rmdir_scanout()

    def test_cmd_noargs(self):
        devnull = open(os.devnull, 'w')
        s = bmd.cmd(argv = [], outs = devnull)
        self.assertEqual(s, 1)
        devnull.close()

    def test_cmd_scan(self):
        argv = ['scan', '-i', self.dirpath('gendoc'), '-o', self.dirpath('scan.out')]
        r = bmd.cmd(argv)
        self.assertEqual(r, 0)
        self.rmdir_scanout()
