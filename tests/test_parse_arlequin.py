from oldowan.arlequin.parse import parse_profile
from oldowan.arlequin.parse import parse_data
from oldowan.arlequin.parse import parse_arlequin

WHOLE_ENTRY="""[Profile]
	Title="A series of simulated samples"
	NbSamples=2

	GenotypicData=1
	GameticPhase=1
	RecessiveData=0
	DataType=STANDARD
	LocusSeparator=WHITESPACE
	MissingData='?'

[Data]
	[[Samples]]


		SampleName="Sample 1"
		SampleSize=5
		SampleData= {
1_1	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	T 	G 	G 	A 	C 	T 	A 	
1_2	1	A 	C 	A 	A 	G 	G 	A 	C 	A 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
1_3	1	A 	C 	A 	T 	G 	G 	T 	C 	T 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	T 	
1_4	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	A 	C 	G 	A 	C 	A 	A 	
1_5	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	

}
		SampleName="Sample 2"
		SampleSize=5
		SampleData= {
2_1	1	A 	G 	A 	A 	G 	T 	A 	C 	A 	A 	
		A 	G 	A 	A 	G 	G 	A 	C 	T 	A 	
2_2	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	T 	G 	G 	T 	G 	T 	A 	
2_3	1	T 	C 	A 	A 	G 	G 	A 	G 	T 	A 	
		A 	C 	C 	A 	G 	G 	A 	G 	T 	A 	
2_4	1	A 	C 	A 	T 	G 	G 	A 	G 	T 	A 	
		A 	C 	A 	A 	G 	G 	T 	C 	T 	A 	
2_5	1	T 	C 	A 	A 	G 	G 	A 	C 	A 	T 	
		T 	C 	A 	A 	G 	G 	A 	C 	A 	A 	

}

[[Structure]]

	StructureName="Simulated data"
	NbGroups=1
	Group={
	   "Sample 1"
	   "Sample 2"
	}

"""

PROFILE="""[Profile]
	Title="A series of simulated samples"
	NbSamples=2

	GenotypicData=1
	GameticPhase=1
	RecessiveData=0
	DataType=STANDARD
	LocusSeparator=WHITESPACE
	MissingData='?'

"""

DATA="""[Data]
	[[Samples]]


		SampleName="Sample 1"
		SampleSize=5
		SampleData= {
1_1	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	T 	G 	G 	A 	C 	T 	A 	
1_2	1	A 	C 	A 	A 	G 	G 	A 	C 	A 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
1_3	1	A 	C 	A 	T 	G 	G 	T 	C 	T 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	T 	
1_4	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	A 	C 	G 	A 	C 	A 	A 	
1_5	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	

}
		SampleName="Sample 2"
		SampleSize=5
		SampleData= {
2_1	1	A 	G 	A 	A 	G 	T 	A 	C 	A 	A 	
		A 	G 	A 	A 	G 	G 	A 	C 	T 	A 	
2_2	1	A 	C 	A 	A 	G 	G 	A 	C 	T 	A 	
		A 	C 	A 	T 	G 	G 	T 	G 	T 	A 	
2_3	1	T 	C 	A 	A 	G 	G 	A 	G 	T 	A 	
		A 	C 	C 	A 	G 	G 	A 	G 	T 	A 	
2_4	1	A 	C 	A 	T 	G 	G 	A 	G 	T 	A 	
		A 	C 	A 	A 	G 	G 	T 	C 	T 	A 	
2_5	1	T 	C 	A 	A 	G 	G 	A 	C 	A 	T 	
		T 	C 	A 	A 	G 	G 	A 	C 	A 	A 	

}

[[Structure]]

	StructureName="Simulated data"
	NbGroups=1
	Group={
	   "Sample 1"
	   "Sample 2"
	}

"""

def test_parse_profile():
    """Parse arlequin profile section."""
    d = parse_profile(PROFILE)
    profile_assertions(d)

def profile_assertions(d):
    assert isinstance(d, dict)
    
    # Mandatory section
    assert d['Title'] is not None
    assert d['NbSamples'] is not None
    assert d['DataType'] is not None
    assert d['GenotypicData'] is not None

    assert isinstance(d['Title'], str)
    assert isinstance(d['NbSamples'], int)
    assert isinstance(d['DataType'], str)
    assert d['GenotypicData'] in [True, False]

    assert "A series of simulated samples" == d['Title']
    assert 2 == d['NbSamples']
    assert 'STANDARD' == d['DataType']
    assert d['GenotypicData']

    # Optional section
    assert d['LocusSeparator'] == 'WHITESPACE'
    assert d['GameticPhase'] 
    assert not d['RecessiveData']
    assert d['RecessiveAllele'] == 'null'
    assert d['MissingData'] == '?'
    assert d['Frequency'] == 'ABS'
    assert not d['CompDistMatrix']
    assert d['FrequencyThreshold'] == 1e-5
    assert d['EpsilonValue'] == 1e-7

def test_parse_data_samples_section():
    """Parse arlequin required data Samples section."""
    d = parse_data(DATA, genotypic=True)
    data_assertions(d)

def data_assertions(d):
    assert isinstance(d, dict)

    assert d.has_key('Samples')
    assert isinstance(d['Samples'], list)

    assert 2 == len(d['Samples'])

    for s in d['Samples']:
        assert isinstance(s, dict)

        assert s.has_key('SampleName')
        assert s.has_key('SampleSize')
        assert s.has_key('SampleData')

        assert isinstance(s['SampleName'], str)
        assert isinstance(s['SampleSize'], int)
        assert isinstance(s['SampleData'], list)

    s1 = d['Samples'][0]
    s2 = d['Samples'][1]

    assert s1['SampleName'] == 'Sample 1' 
    assert s1['SampleSize'] == 5
    assert 5 == len(s1['SampleData'])
    for x in s1['SampleData']:
        assert isinstance(x, dict)
        assert x.has_key('name')
        assert x.has_key('frequency')
        assert x.has_key('data')
        assert 2 == len(x['data'])
        for d in x['data']:
            assert 10 == len(d.split())

    assert s2['SampleName'] == 'Sample 2'
    assert s2['SampleSize'] == 5
    assert 5 == len(s2['SampleData'])
    for x in s2['SampleData']:
        assert isinstance(x, dict)
        assert x.has_key('name')
        assert x.has_key('frequency')
        assert x.has_key('data')
        assert 2 == len(x['data'])
        for d in x['data']:
            assert 10 == len(d.split())
  
def test_parse_whole_entry():
    """Parse the whole arlequin entry."""
    d = parse_arlequin(WHOLE_ENTRY)
    assert isinstance(d, dict)

    assert d.has_key('Profile')
    profile_assertions(d['Profile'])

    assert d.has_key('Data')
    data_assertions(d['Data'])

