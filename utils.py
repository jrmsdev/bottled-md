import time
from os import path


class _G:
    """global namespace"""
    scan_mode = False
    dstdir = None
    dst_fpath = None


def timefmt(epoch, fmt = '%a, %d %b %Y %T %z'):
    """return formatted time string"""
    t = time.localtime(epoch)
    return time.strftime(fmt, t)


def url(relpath):
    if _G.scan_mode:
        doc_dir = path.dirname(_G.dst_fpath)
        reldir = ''
        if doc_dir != _G.dstdir:
            dots = len(doc_dir.replace('%s/' % _G.dstdir, '', 1).split(path.sep))
            for _ in range(0, dots):
                reldir = '../%s' % reldir
        return '%s%s' % (reldir, relpath)
    else:
        return '/%s' % relpath


def static_url(fname):
    return url('static/%s' % fname)


def tpl_dict():
    """map utilities in a dictionary"""
    return dict(
        timefmt = timefmt,
        url = url,
        static_url = static_url,
    )


def scan_mode(dstdir, dst_fpath):
    """prepare utils for scan mode"""
    _G.scan_mode = True
    _G.dstdir = path.abspath(dstdir)
    _G.dst_fpath = path.abspath(dst_fpath)
