__all__ = ['parse_arlequin']

import re

def parse_arlequin(entry):
    """Parse a block of Arlequin formatted text."""
    if not entry.upper().startswith('[PROFILE]'):
        raise TypeError("entry does not start with '[Profile]'")

    parsed = {}

    sections = [ x.strip() for x in RE_SECTIONS.split(entry) if len(x.strip()) != 0 ]

    for s in sections:
        if s.upper().startswith('[PROFILE]'):
            parsed['Profile'] = parse_profile(s)
        elif s.upper().startswith('[DATA]'):
            parsed['Data'] = parse_data(s, parsed['Profile']['GenotypicData'])

    return parsed

def parse_arlequin_results(results_text):
    """Parse a block of Arlequin results text."""
    raise NotImplementedError

    
# 
# PRIVATE UTILITY FUNCTIONS USED IN PARSER
#
# These functions are implementation details and should not be used outside of
# this parser. There is no guarantee that any of these will be maintained or
# necessarily function the same as the parser evolves. The call signature and
# return values of the 'parse_arlequin' function are the only supported public
# interface.
#

def parse_profile(profile_text):
    parsed =   {'Title': None,
            'NbSamples': None,
             'DataType': None,
        'GenotypicData': None,
       'LocusSeparator': 'WHITESPACE',
         'GameticPhase': True,
        'RecessiveData': False,
      'RecessiveAllele': 'null',
          'MissingData': '?',
            'Frequency': 'ABS',
       'CompDistMatrix': False,
   'FrequencyThreshold': 1e-5,
         'EpsilonValue': 1e-7}
    for line in RE_NEWLINE.split(profile_text):
        if '=' in line:
            key, val = line.strip().split('=', 1)
            if parsed.has_key(key):
                parsed[key] = convert(key, val)
    return parsed

def parse_data(data_text, genotypic):
    """Parse the entire Data section."""
    parsed = {}
    # first result of the split is just the '[Data]' line,
    # so discard that
    sections = RE_DATA_SUBDIV.split(data_text)[1:]
    for s in sections:
        if RE_SAMPLES.match(s):
            parsed['Samples'] = parse_samples(s, genotypic)
    return parsed

def parse_samples(samples_text, genotypic):
    """Parse the entire Samples sub-section."""
    extracted = RE_SAMPLE.findall(samples_text)
    samples = []
    for s in extracted:
        samples.append(parse_sample(s, genotypic))
    return samples

def parse_sample(sample_text, genotypic):
    """Parse a single Sample."""
    d = {}
    d['SampleName'] = clean_up(RE_SAMPLENAME.search(sample_text).group(1))
    d['SampleSize'] = int(RE_SAMPLESIZE.search(sample_text).group(1))
    d['SampleData'] = parse_sampledata(RE_SAMPLEDATA.search(sample_text).group(1), genotypic)
    return d

def parse_sampledata(sd_text, genotypic):
    # first, strip whitespace
    txt = sd_text.strip()
    # next, split the lines
    lines = RE_NEWLINE.split(txt)
    # a list to put everything in
    individuals = []
    if genotypic:
        # individuals take two lines each
        for i in range(0,len(lines),2):
            name, freq, g1 = lines[i].split(None, 2)
            g2 = lines[i+1].strip()
            individuals.append({'name': name,
                                'frequency': int(freq),
                                'data': [g1, g2]})
    else:
        # each individual is on a line
        for line in lines:
            name, freq, data = line.split(None, 2)
            individuals.append({'name': name,
                                'frequency': int(freq),
                                'data': data})
    return individuals

def clean_up(strng):
    """Strip excess whitespace and de-quote a string."""
    strng = strng.strip()
    # remove opening and closing "s or 's if present
    quote_mo = RE_DOUBLE_QUOTED.match(strng)
    if quote_mo:
        strng = quote_mo.group(1)
    else:
        quote_mo = RE_SINGLE_QUOTED.match(strng)
        if quote_mo:
            strng = quote_mo.group(1)
    return strng

def convert(key, val):
    """Convert strings as read to string, int, bool as necessary."""
    if PROFILE_TYPES[key] == str:
        return clean_up(val)
    elif PROFILE_TYPES[key] == bool:
        return val == '1'
    elif PROFILE_TYPES[key] == int:
        return int(val)
    elif PROFILE_TYPES[key] == float:
        return float(val)

#
# REGULAR EXPRESSIONS USED IN PARSER
#

#: Match newlines
RE_NEWLINE       = re.compile(r'\r\n|\r|\n')

#: Match "quoted" or 'quoted' text, capturing the inner text
RE_DOUBLE_QUOTED = re.compile(r'^"(.*?)"$')
RE_SINGLE_QUOTED = re.compile(r"^'(.*?)'$")

#: Match sections
RE_SECTIONS      = re.compile(r'(^|[\r\n]+)(?=\[\w)')

#: Match subsections in Data section
RE_DATA_SUBDIV   = re.compile(r'[\r\n]\s*(?=\[\[)')

#: Match Data Samples subsection
RE_SAMPLES       = re.compile(r'\s*\[\[Samples\]\]')

#: Match inidividual Sample subsection
RE_SAMPLE        = re.compile(r'Sample.*?}', re.S)

#: Extract SampleName from Sample sub-section
RE_SAMPLENAME    = re.compile(r'SampleName\s*=\s*(.*)')

#: Extract SampleSize from Sample sub-section
RE_SAMPLESIZE    = re.compile(r'SampleSize\s*=\s*(\d+)')

#: Extract SampleData from Sample sub-section
RE_SAMPLEDATA    = re.compile(r'SampleData\s*=\s*{([^}]+)', re.S)

#: Extract individual from SampleData
RE_SAMPLE_INDIVIDUAL = re.compile(r'', re.S)

#
# CONSTANTS USED IN PARSING
#

PROFILE_TYPES ={'Title': str,
            'NbSamples': int,
             'DataType': str,
        'GenotypicData': bool,
       'LocusSeparator': str,
         'GameticPhase': bool,
        'RecessiveData': bool,
      'RecessiveAllele': str,
          'MissingData': str,
            'Frequency': str,
       'CompDistMatrix': bool,
   'FrequencyThreshold': float,
         'EpsilonValue': float}
