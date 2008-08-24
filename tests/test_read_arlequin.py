from oldowan.arlequin import iterate_arlequin
from oldowan.arlequin import read_arlequin

import os

SNPS_TWO_POPS = os.path.join(os.path.dirname(__file__), 
        'test_files', 'snps_two_pops.arp')

f = open(SNPS_TWO_POPS, 'r')
SNPS_TWO_POPS_TEXT = f.read()
f.close()

def test_iterate_arlequin_from_text():
    """read_arlequin given text"""
    # first, tell it what's going on
    d = read_arlequin(SNPS_TWO_POPS_TEXT, what='text')
    assert isinstance(d, list)

    # next, make it guess
    d = read_arlequin(SNPS_TWO_POPS_TEXT)
    assert isinstance(d, list)

def test_iterate_arlequin_from_filename():
    """read_arlequin given filename"""
    # first, tell it what's going on
    d = read_arlequin(SNPS_TWO_POPS, what='filename')
    assert isinstance(d, list)

    # next, make it guess
    d = read_arlequin(SNPS_TWO_POPS)
    assert isinstance(d, list)

def test_iterate_arlequin_from_file():
    """read_arlequin given file"""
    f = open(SNPS_TWO_POPS, 'r')
    # first, tell it what's going on
    d = read_arlequin(f, what='file')
    assert isinstance(d, list)

    f = open(SNPS_TWO_POPS, 'r')
    # next, make it guess
    d = read_arlequin(f)
    assert isinstance(d, list)

def test_iterate_arlequin_with_dict_return():
    """iterate_arlequin with default options"""
    for entry in iterate_arlequin(SNPS_TWO_POPS_TEXT):
        assert isinstance(entry, dict)

def test_iterate_arlequin_with_raw_return():
    """iterate_arlequin with raw option"""
    for entry in iterate_arlequin(SNPS_TWO_POPS_TEXT, raw=True):
        assert isinstance(entry, str)

