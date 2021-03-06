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
import utils


# bottle templates dir
bottle.TEMPLATE_PATH.insert(0, path.join(path.dirname(__file__), 'templates'))

app = bottle.Bottle()
bottle.app.push(app)


def tpl_utils(func):
    """decorator: add utilities to be used on templates"""
    def wrapped(*args, **kwargs):
        d = func(*args, **kwargs)
        d.update(utils.tpl_dict())
        return d
    return wrapped


def tpl_data(doc_path):
    """decorator: common data for templates"""
    def decorator(func):
        def wrapped(*args, **kwargs):
            d = func(*args, **kwargs)
            d.update(dict(
                doc_path = doc_path,
                doc_mtime = os.stat(doc_path).st_mtime,
                time_now = time.time(),
            ))
            return d
        return wrapped
    return decorator


# list of static dirs: internal and custom
static_dirs = {
    'int': path.join(path.dirname(__file__), 'static'),
    'src': None,
}

@bottle.route('/static/<fpath:path>')
def static(fpath):
    # source first, internal otherwise
    for d in (static_dirs['src'], static_dirs['int']):
        if d:
            f = path.join(d, fpath)
            if path.isfile(f):
                return bottle.static_file(fpath, root = d)
    bottle.abort(404, 'file not found: %s' % fpath)


def gendoc(fpath, md_extensions = []):
    """generate html doc as string from source markdown file"""

    @bottle.view('htdoc_head')
    @tpl_data(fpath)
    @tpl_utils
    def htdoc_head():
        """render htdoc head template"""
        return dict()

    @bottle.view('htdoc_tail')
    @tpl_data(fpath)
    @tpl_utils
    def htdoc_tail():
        """render htdoc tail template"""
        return dict()

    # parse markdown file
    buf = io.BytesIO()
    try:
        markdownFromFile(input = fpath, extensions = md_extensions,
                output = buf, output_format = 'html5')
    except FileNotFoundError as err:
        bottle.abort(404, str(err))

    # generate response
    buf.seek(0, 0)
    return htdoc_head() + buf.read().decode() + htdoc_tail()

def static_mimetype(fpath):
    mtype = 'application/actet-stream'
    ext = fpath[-4:]
    if ext == '.txt' or ext == '.pxd':
        mtype = 'text/plain'
    return mtype


@bottle.route('/<fpath:path>')
def serve_doc(fpath):
    if not path.isfile (fpath):
        """check path is a file"""
        bottle.abort(404, 'file not found: %s' % fpath)

    if fpath[-3:] == '.md':
        return gendoc(fpath)

    # serve static files
    return bottle.static_file(fpath, root = '.',
                              mimetype = static_mimetype(fpath))


@bottle.route('/')
def index():
    for src in ('index.md', 'README.md'):
        try:
            if os.stat(src):
                return gendoc(src)
        except FileNotFoundError:
            pass
    bottle.abort(404, 'no index document found')


def sync_static(src, dst):
    """copy static files from src dir to dst (not recursively)"""
    for f in os.listdir(src):
        src_f = path.join(src, f)
        dst_f = path.join(dst, f)
        if path.isfile(src_f):
            if not path.isdir(dst):
                os.makedirs(dst)
            with open(dst_f, 'w') as fw:
                with open(src_f, 'r') as fr:
                    fw.write(fr.read())
                    fr.close()
                fw.close()


def scan(srcdir, dstdir, debug = False):
    """scan source directory for .md files and generate .html docs in destination"""

    def writedoc():
        """write html5 file"""
        d = path.dirname(src_f.replace(srcdir, dstdir, 1))
        f = path.basename(src_f).replace('.md', '.html')
        dst_f = path.join(d, f)

        if debug:
            print (src_f, '->', dst_f)

        try:
            os.makedirs(path.dirname(dst_f))
        except FileExistsError:
            pass

        # set utils in scan mode
        utils.scan_mode(dstdir, dst_f)

        # gendoc and write it
        with open(dst_f, 'w') as fh:
            fh.write(gendoc(src_f, [mdx.MDX()]))
            fh.close()

    # scan source directory for .md source files
    for src_f in glob('%s/**/*.md' % srcdir, recursive = True):
        writedoc()

    # sync static files
    for sdir in static_dirs.values():
        if sdir is not None:
            sync_static(sdir, path.join(dstdir, 'static'))

    return 0


def cmd(argv = sys.argv[1:], outs = sys.stdout):
    parser = OptionParser(usage = '%prog [options] scan|serve')
    parser.add_option('-d', '--debug', action = 'store_true', default = False,
            help = 'enable debug options')
    parser.add_option('-p', '--http', metavar = 'PORT', default = 8880,
            help = 'bottle http port to bind to (default: 88880)', type = int)
    parser.add_option('-i', '--srcdir', metavar = 'SRCDIR',
            help = "source directory (default: '.')", default = '.')
    parser.add_option('-o', '--dstdir', metavar = 'DSTDIR',
            help = "destination directory (default: 'htdocs')", default = 'htdocs')
    opts, args = parser.parse_args(argv)

    if len(args) == 1:

        # allow source dir templates
        tpldir = path.abspath(path.join(opts.srcdir, 'templates'))
        if path.isdir(tpldir):
            bottle.TEMPLATE_PATH.insert(0, tpldir)

        # register source static dir
        sdir = path.abspath(path.join(opts.srcdir, 'static'))
        if path.isdir(sdir):
            static_dirs['src'] = sdir

        # scan
        if args[0] == 'scan':
            # generate static docs
            scan(opts.srcdir, opts.dstdir, debug = opts.debug)
            return 0

        # serve
        elif args[0] == 'serve':
            # chdir and run bottle
            os.chdir(opts.srcdir)
            return bottle.run(host = 'localhost', port = opts.http,
                              reloader = opts.debug, debug = opts.debug)

        # invalid arg
        else:
            parser.print_help(file = outs)
            return 2

    # no args
    parser.print_help(file = outs)
    return 1


if __name__ == '__main__':
    sys.exit(cmd())
