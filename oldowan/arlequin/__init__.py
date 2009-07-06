"""This is the OldowanArlequin package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['arlequin'] 


try:
    from oldowan.arlequin.arlequin import arlequin
    #from oldowan.arlequin.arlequin import parse_arlequin
    #from oldowan.arlequin.arlequin import entry2str
except:
    from arlequin import arlequin
    #from arlequin import parse_arlequin
    #from arlequin import entry2str
