"""Make sure functions do what they say
"""

from nose.tools import raises

from ..parser import SpecfitParser
from ..tools import check_db_diff, reset_failed_parameters
from data import *

#-------------------------------------------------------------------------------

class test_diff():

    def test_no_diff(self):
        """Databases with no differences"""
        assert check_db_diff(COMPONENT_FILE, COMPONENT_FILE) == 0, "Differences found in identical file"

        assert check_db_diff(SpecfitParser(COMPONENT_FILE),
                             SpecfitParser(COMPONENT_FILE)) == 0, "Differences found in identical db in memory"

#-------------------------------------------------------------------------------

class test_reset_failed_parameters():

    def test_correct_change(self):
        """failed database is reset"""
        db = SpecfitParser(COMPONENT_FILE)

        db[0][0].value = db[0][0].upper_lim *2
        db[1][1].value = .9 * db[1][1].upper_lim

        out = COMPONENT_FILE + '_out'
        db.write(out)

        assert check_db_diff(COMPONENT_FILE, out) == 2, "Differences not propogated"
        reset_failed_parameters(out, COMPONENT_FILE)
        assert check_db_diff(COMPONENT_FILE, out) == 0, "Data not reset correctly"

        os.remove(out)

#-------------------------------------------------------------------------------
