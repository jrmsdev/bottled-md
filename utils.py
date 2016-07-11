import time

def timefmt(epoch, fmt = '%a, %d %b %Y %T %z'):
    t = time.localtime(epoch)
    return time.strftime(fmt, t)
