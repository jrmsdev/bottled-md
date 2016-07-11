import time

def timefmt(epoch, fmt = '%a, %d %b %Y %T %z'):
    """return formatted time string"""
    t = time.localtime(epoch)
    return time.strftime(fmt, t)

def tpl_dict():
    """map utilities in a dictionary"""
    return dict(timefmt = timefmt)
