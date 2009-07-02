import re
import StringIO

class arlequin(object):
    """arlequin(filename_or_data[, mode[, parse]]) -> a arlequin object.

    Create a arlequin object. The mode can be 'r' (reading, default), 
    's' (string data), 'f' (file object), 'a' (append), or 'w' (write).
    The file will be created if it doesn't exist for writing or appending;
    it will be truncated when opened for reading. For read mode, 
    universal newline support is automatically invoked. By default, each
    arlequin entry is parsed into a dict with 'name' and 'sequence'
    values (parse=True). For 'raw' strings, set parse=False."""

    __parse = True
    def __get_parse(self):
        return self.__parse
    def __set_parse(self, value):
        if not isinstance(value, bool):
            raise ValueError("'%s' is not a boolean." % value)
        self.__parse = value
    parse = property(fget=__get_parse,
                     fset=__set_parse,
                     doc="parse entry into dict (default=True)")

    __mode = None
    def __get_mode(self):
        return self.__mode
    mode = property(fget=__get_mode,
                    doc="file mode ('r', 's', 'f', 'w', or 'a')")

    def __get_closed(self):
        return self.__fobj.closed
    closed = property(fget=__get_closed,
                      doc="True if the file is closed")

    __fobj = None
    __buff = 'x' # needs to be initialized with non-zero, non-'>' character

    def __init__(self, 
                 filename_or_data, 
                 mode='r', 
                 parse=True,
                 data_type="DNA",
                 locus_separator="NONE",
                 missing_data="?",
                 title="",
                 num_samples=1,
                 genotypic_data=0):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        if mode[0] in ['r', 'a', 'w']:
            if mode == 'r': 
                # force universal read mode
                mode = 'rU' 
            self.__fobj = open(filename_or_data, mode)
        elif mode == 'f':
            self.__fobj = filename_or_data
        elif mode == 's':
            self.__fobj = StringIO.StringIO(filename_or_data)
        else:
            msg = "mode string must start with 'r', 'a', 'w', 'f' or 's', \
                    not '%s'" % mode[0]
            raise ValueError(msg)
        self.__mode = mode
        self.parse = parse
        
        if mode == 'w':
            self.__write_header(title,num_samples,genotypic_data,data_type,
                    locus_separator,missing_data)

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return self

    def __enter__(self):
        """__enter__() -> self."""
        return self

    def __exit__(self, type, value, traceback):
        """__exit__(*excinfo) -> None.  Closes the file."""
        self.__fobj.close()

    def close(self):
        """close() -> None or (perhaps) an integer.  Close the file."""
        return self.__fobj.close()

    def flush(self):
        """flush() -> None.  Flush the internal I/O buffer."""
        return self.__fobj.flush()

    def next(self):
        """next() -> the next entry, or raise StopIteration"""
        nxt = self.readentry()
        if nxt is None:
            self.__fobj.close()
            raise StopIteration
        return nxt

    def __write_header(self, 
                       title, 
                       num_samples, 
                       genotypic_data, 
                       data_type, 
                       locus_separator,
                       missing_data):
        self.__fobj.write('[Profile]\n')
        self.__fobj.write('\n')
        self.__fobj.write('\tTitle="%s"\n' % title)
        self.__fobj.write('\n')
        self.__fobj.write('\tNbSamples=%d\n' % num_samples)
        self.__fobj.write('\tGenotypicData=%d\n' % genotypic_data)
        self.__fobj.write('\tDataType=%s\n' % data_type)
        self.__fobj.write('\tLocusSeparator=%s\n' % locus_separator)
        self.__fobj.write('\tMissingData="%s"\n' % missing_data)
        self.__fobj.write('\n')
        self.__fobj.write('[Data]\n')
        self.__fobj.write('\n')
        self.__fobj.write('\t[[Samples]]\n')
        self.__fobj.write('\n')
        self.flush()

    def write_sample(self, sample_name, sample_data):
        self.__fobj.write('\t\tSampleName="%s"\n' % sample_name)
        self.__fobj.write('\t\tSampleSize=%d\n' % len(sample_data))
        self.__fobj.write('\t\tSampleData={\n')
        for entry in sample_data:
            self.__fobj.write('%s\t%d\t%s\n' % (entry['id'], entry['n'], entry['value']))
        self.__fobj.write('}\n')
        self.__fobj.write('\n')

