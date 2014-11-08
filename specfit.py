
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

        self.parameters = [SpecfitParameter(line) for line in lines[1:]]

    def __str__(self):
        return "component: {} #{}".format(self.type, self.number)

#-------------------------------------------------------------------------------

class SpecfitParameter:
    """Parse and modify a parameter of a compenent"""

    def __init__(self, line):
        values = line.strip().split()

        if len(values) != 6:
            raise ValueError('Parameter can only have 6 values!')

        self.value = float(values[0])
        self.lower_lim = float(values[1])
        self.upper_lim = float(values[2])
        self.stepsize = float(values[3])
        self.toleranse = float(values[4])
        self.linkage = float(values[5])



#-------------------------------------------------------------------------------
