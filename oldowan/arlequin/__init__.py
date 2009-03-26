"""This is the OldowanArlequin package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['read_arlequin', 
           'iterate_arlequin', 
           'parse_arlequin', 
           'write_arlequin']

from oldowan.arlequin.read import read_arlequin
from oldowan.arlequin.iterate import iterate_arlequin
from oldowan.arlequin.parse import parse_arlequin
from oldowan.arlequin.write import write_arlequin

