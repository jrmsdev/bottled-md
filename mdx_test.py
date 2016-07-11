import os
from os import path
from unittest import TestCase

import bmd
import mdx

class TestMDX(TestCase):

    def dirpath(self, dname):
        return path.join(path.dirname(__file__), 'testdata', dname)

    def chdir(self, dname):
        os.chdir(self.dirpath(dname))

    def test_local_links(self):
        self.chdir('local-links')
        d = bmd.gendoc('index.md', md_extensions = [mdx.MDX()])
        self.assertIsInstance(d, str)
        self.assertEqual(len(d), 400)
