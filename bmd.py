#!/usr/bin/env python3

import io
import os
import sys
import time
import bottle

from os import path
from glob import glob
from optparse import OptionParser
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
        return dict(
            doc_mtime = os.stat(fpath).st_mtime,
            time_now = time.time(),
        )

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


@bottle.route('/')
def index():
    for src in ('index.md', 'README.md'):
        try:
            if os.stat(src):
                return gendoc(src)
        except FileNotFoundError:
            pass
    bottle.abort(404, 'no index document found')


def scan(srcdir, dstdir):
    """scan source directory for .md files and generate .html docs in destination"""

    def writedoc():
        """write html5 file"""
        dst_f = path.join(dstdir, src_f.replace('.md', '.html'))
        try:
            os.makedirs(path.dirname(dst_f))
        except FileExistsError:
            pass
        with open(dst_f, 'w') as fh:
            fh.write(gendoc(src_f, md_extensions))
            fh.close()
            print(src_f)

    # markdown extensions
    md_extensions = [mdx.MDX()]

    # scan source directory for .md source files
    for src_f in glob('%s/**/*.md' % srcdir, recursive = True):
        writedoc()

    return 0


def cmd():
    parser = OptionParser(usage = '%prog [options] scan|serve')
    parser.add_option('-d', '--debug', action = 'store_true', default = False,
            help = 'enable debug options')
    parser.add_option('-p', '--http', metavar = 'PORT', default = 8880,
            help = 'bottle http port to bind to (default: 88880)', type = int)
    parser.add_option('-i', '--srcdir', metavar = 'SRCDIR',
            help = "source directory (default: '.')", default = '.')
    parser.add_option('-o', '--dstdir', metavar = 'DSTDIR',
            help = "destination directory (default: 'htdocs')", default = 'htdocs')
    opts, args = parser.parse_args()

    if args:
        # allow source dir templates
        tpldir = path.abspath(path.join(opts.srcdir, 'templates'))
        if path.isdir(tpldir):
            bottle.TEMPLATE_PATH.insert(0, tpldir)

        if args[0] == 'scan':
            # generate static docs
            sys.exit(scan(opts.srcdir, opts.dstdir))
        elif args[0] == 'serve':
            # start bottle
            bottle.run(host = 'localhost', port = opts.http,
                    reloader = opts.debug, debug = opts.debug)
        else:
            parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    cmd()
