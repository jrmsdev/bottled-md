#!/usr/bin/env python3

import io
import os
import sys
import time
import bottle

from os import path
from glob import glob
from markdown import markdownFromFile

import mdx


# bottle templates dir
bottle.TEMPLATE_PATH.insert(0, path.dirname(__file__))

app = bottle.Bottle()
bottle.app.push(app)


def tpl_utils(func):
    """add utilities to be used on templates"""

    def timefmt(fmt, epoch):
        t = time.localtime(epoch)
        return time.strftime(fmt, t)

    utils = dict(timefmt = timefmt)

    def wrapped(*args, **kwargs):
        d = func(*args, **kwargs)
        d.update(utils)
        return d

    wrapped.__name__ = func.__name__
    wrapped.__doc__ = func.__doc__

    return wrapped


@bottle.route('/<fpath:path>')
def gendoc(fpath, md_extensions = []):
    """generate html doc as string from source markdown file"""

    @bottle.view('htdoc_head')
    def htdoc_head():
        """render htdoc head template"""
        return dict(doc_fpath = fpath)

    @bottle.view('htdoc_tail')
    @tpl_utils
    def htdoc_tail():
        """render htdoc tail template"""
        return dict(doc_mtime = os.stat(fpath).st_mtime)

    # parse markdown file
    buf = io.BytesIO()
    try:
        markdownFromFile(input = fpath, extensions = md_extensions,
                output = buf, output_format = 'html5')
    except FileNotFoundError as err:
        bottle.abort(404, str(err))
    else:
        buf.seek(0, 0)

    # generate response
    return htdoc_head() + buf.read().decode() + htdoc_tail()


def main(outdir = 'htdocs'):
    """scan current directory for .md files and generate .html docs"""

    def writedoc():
        """write html5 file"""
        dst_f = path.join(outdir, src_f.replace('.md', '.html'))
        try:
            os.makedirs(path.dirname(dst_f))
        except FileExistsError:
            pass
        with open(dst_f, 'w') as fh:
            fh.write(gendoc(src_f, md_extensions))
            fh.close()

    md_extensions = [mdx.MDX()]

    # scan current directory for .md source files
    for src_f in glob('**/*.md', recursive = True):
        writedoc()

    return 0


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-d', '--debug', action = 'store_true', default = False,
            help = 'enable debug options')
    parser.add_option('-p', '--http', metavar = 'PORT',
            help = 'start bottle server to dinamically serve content')
    opts, _ = parser.parse_args()

    if opts.http:
        # start bottle
        bottle.run(host = 'localhost', port = opts.http,
                reloader = opts.debug, debug = opts.debug)
    else:
        # generate static docs
        sys.exit(main())
