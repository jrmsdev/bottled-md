#!/usr/bin/env python3

import io
import os
import sys
import bottle

from os import path
from glob import glob
from markdown import markdownFromFile

#~ from optparse import OptionParser

# bottle templates dir
bottle.TEMPLATE_PATH.insert(0, path.dirname(__file__))

app = bottle.Bottle()
bottle.app.push(app)


@bottle.route('/<fpath:path>')
def gendoc(fpath):
    """generate html doc as string from source markdown file"""

    @bottle.view('htdoc_head')
    def htdoc_head():
        """render htdoc head template"""
        return dict(doc_fpath = fpath)

    @bottle.view('htdoc_tail')
    def htdoc_tail():
        """render htdoc tail template"""
        return dict()

    # parse markdown file
    buf = io.BytesIO()
    markdownFromFile(input = fpath, output = buf)
    buf.seek(0, 0)

    # generate response
    return htdoc_head() + buf.read().decode() + htdoc_tail()


def main():
    """generate html5 files from markdown sources"""

    def writedoc(fpath):
        """write html5 file"""
        dst_f = path.join('htdocs', fpath.replace('.md', '.html'))
        try:
            os.makedirs(path.dirname(dst_f))
        except FileExistsError:
            pass
        with open(dst_f, 'w') as fh:
            fh.write(gendoc(fpath))
            fh.close()

    for src_f in glob('**/*.md', recursive = True):
        writedoc(src_f)

    return 0


if __name__ == '__main__':
    sys.exit(main())
