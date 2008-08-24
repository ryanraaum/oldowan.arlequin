__all__ = ['read_arlequin']

from oldowan.arlequin.iterate import iterate_arlequin

def read_arlequin(something, what='guess', raw=False):
    """Read the Arlequin input format."""
    items = []

    for entry in iterate_arlequin(something, what, raw):
        items.append(entry)

    return items

def read_arlequin_results(something, what='guess', raw=False):
    """Read Arlequin results."""
    raise NotImplementedError
