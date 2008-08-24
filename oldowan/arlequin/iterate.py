
__all__ = ['iterate_arlequin']

from oldowan.arlequin.parse import parse_arlequin

import re, StringIO

def iterate_arlequin(something, what='guess', raw=False):
    """Iterate through blocks of Arlequin format."""
    if what == 'guess':
        if type(something) == file:
            what = 'file'
        elif type(something) == str:
            if len(something) > 256:
                what = 'text'
            else:
                what = 'filename'
    if what == 'file':
        f = something
    elif what == 'filename':
        f = open(something, 'r')
    elif what == 'text':
        f = StringIO.StringIO(something)
    else:
        raise TypeError("don't know how to handle '%s'" % what)
  
    # find the beginning of the first entry
    buf = ''
    while not buf.upper().startswith('[PROFILE]'):
        buf = f.readline()

    if buf == '':
        f.close()
        raise IOError("file '%s' does not appear to be in Arlequin format" % filename)

    done = False
    while not done:
        entry = []
        while buf != '':
            entry.append(buf)
            buf = f.readline()
            # read until the next entry ('[PROFILE]') or end of file ('')
            if buf.upper().startswith('[PROFILE]') or buf == '':
                if raw:
                    yield ''.join(entry)
                else:
                    yield parse_arlequin(''.join(entry))
                entry = []
        f.close()
        done = True

def iterate_arlequin_results(something, what='guess', raw=False):
    """Iterate through blocks of Arlequin results."""
    raise NotImplementedError

