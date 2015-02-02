"""Make sure reading and writing is working fine
"""

from nose.tools import raises

from ..parser import SpecfitParser
from ..tools import check_db_diff
from data import *

#-------------------------------------------------------------------------------

class test_read():

    def test_read_valid(self):
        """Read in a valid db file"""
        assert SpecfitParser(COMPONENT_FILE), "Failed to read in the valid file."


    @raises(ValueError)
    def test_read_blank(self):
        """Read in a blank db file"""
        SpecfitParser(BLANK_FILE)
        SpecfitParser(BLANK_COMPONENT_FILE)

#-------------------------------------------------------------------------------

class test_write():

    def test_write_nochange(self):
        """Write a valid db file with no change"""
        db = SpecfitParser(COMPONENT_FILE)

        outfile = COMPONENT_FILE + '_out'
        db.write(outfile)

        n_diff = check_db_diff(COMPONENT_FILE, outfile)
        assert n_diff == 0, "DB changed upon output, {} differences".format(n_diff)
        os.remove(outfile)


    def test_write_change(self):
        """Write a valid db file containing a modiciation"""
        db = SpecfitParser(COMPONENT_FILE)

        db[0][0].value = 5

        outfile = COMPONENT_FILE + '_out'
        db.write(outfile)

        n_diff = check_db_diff(db, outfile)
        assert n_diff == 0, "Change not propogated to output. {} differnces".format(n_diff)
        os.remove(outfile)

#-------------------------------------------------------------------------------
