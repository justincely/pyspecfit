
class SpecfitParser:
    """Parse and modify parameter files for the SpecFit task"""

    def __init__(self, filename):
        pass

    def read(self):
        pass

#-------------------------------------------------------------------------------

class SpecfitComponent:
    """Parse and modify an individual compenent of a SpecFit paramter file"""

    def __init__(self, lines):
        self.name, self.n_pars = lines[0].strip().split()[0:2]
        self.n_pars = int(self.n_pars)
        self.label = ''.join(lines[0].strip().split()[3:]) or 'None'

        #-- Strip out numbers to get type of model fit
        #-- ALL numbers will be stripped, but they should all be at the end
        self.type = ''.join([item for item in self.name if not item.isdigit()])
        self.number = int(''.join([item for item in self.name if item.isdigit()]))

        if self.n_pars != len(lines[1:]):
            message = "Incorrect number of parameters specified for"
            message += "{}, got {} instead of {}".format(self.type,
                                                         len(lines[1:]),
                                                         self.n_pars)
            raise ValueError(message)
