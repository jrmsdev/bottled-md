#!/usr/bin/env python3

from unittest import TestLoader

ldr = TestLoader()
suite = ldr.discover('.', '*_test.py')

if __name__ == '__main__':
    import sys
    from unittest import TextTestRunner

    verbose = 1
    if '-v' in sys.argv:
        verbose = 2

    rnr = TextTestRunner(verbosity=verbose)
    rst = rnr.run(suite)

    sys.exit(len(rst.errors))
