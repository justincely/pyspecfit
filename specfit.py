import os
from datetime import datetime

#-------------------------------------------------------------------------------

class SpecfitParser:
    """Parse and modify parameter files for the SpecFit task"""

    def __init__(self, filename):
        self.filename = filename
        self.n_components = 0
        self.components = {}

        self.loadfile()

    def __str__(self):
        message = "Specfit database file {}\n".format(self.filename)
        message += '\n'.join(['-' + str(item) for item in self.components])
        return message

    def __iter__(self):
        for item in self.components.itervalues():
            yield item

    def loadfile(self):
        data = open(self.filename).readlines()

        if not len(data):
            raise ValueError('No lines in input datafile')

        for i, line in enumerate(data):
            line = line.strip()
            if line.startswith('components'):
                self.n_components = int(line.split()[1])
                self.read_components(data, i + self.n_components + 1)
                return

        raise ValueError('No components found')

    def read_components(self, data, start):
        components_read = 0

        while components_read < self.n_components:
            comp_name, n_pars = data[start].strip().split()[0:2]
            n_pars = int(n_pars)

            if comp_name in self.components:
                raise KeyError('Component defined twice!')

            self.components[comp_name] = SpecfitComponent(data[start:start + n_pars + 1])

            components_read += 1
            start += n_pars + 1

        if components_read < self.n_components:
            raise ValueError("Not enough parameters supplied")


    def write(self, outname, clobber=False, mode='w'):
        if os.path.exists(outname) and not clobber:
            raise IOError("Will not overrite {} while clobber={}".format(outname,
                                                                         clobber))

        now = datetime.now()

        with open(outname, mode) as out_file:
            #-- Not sure if these are needed, keeping for now
            out_file.write('# {}\n'.format(now.ctime()))
            out_file.write('being {}\n'.format(outname))
            out_file.write('      task    specfit\n')

            #-- These are needed
            out_file.write('components    {}\n'.format(self.n_components))

            for item in self.components.itervalues():
                out_file.write('         {}\n'.format(item.type))

            for item in self.components.itervalues():
                out_file.write('{:>19}    {} # {}\n'.format(item.name,
                                                           item.n_pars,
                                                           item.label))
                for par in item.parameters:
                    out_file.write('{:>33}{:>10}{:>10}{:>10}{:>10}{:>10}\n'.format(par.value,
                                                                              par.lower_lim,
                                                                              par.upper_lim,
                                                                              par.stepsize,
                                                                              par.tolerance,
                                                                              par.linkage))

#-------------------------------------------------------------------------------

class SpecfitComponent:
    """Parse and modify an individual compenent of a SpecFit paramter file"""

    def __init__(self, lines):
        self.name, self.n_pars = lines[0].strip().split()[0:2]
        self.n_pars = int(self.n_pars)
        self.label = ''.join(lines[0].strip().split()[3:]) or ''

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
        output = "component: {} #{}\n".format(self.type, self.number)
        output += '\n'.join(['--' + str(item) for item in self.parameters])
        return output


    def __iter__(self):
        for item in self.parameters:
            yield item

#-------------------------------------------------------------------------------

class SpecfitParameter:
    """Parse and modify a parameter of a compenent"""

    def __init__(self, line):
        values = map(float, line.strip().split())

        if len(values) != 6:
            raise ValueError('Parameter can only have 6 values!')

        self.value = values[0]
        self.lower_lim = values[1]
        self.upper_lim = values[2]
        self.stepsize = values[3]
        self.tolerance = values[4]
        self.linkage = values[5]

    def __str__(self):
        return "parameter: {} {} {} {} {} {}".format(self.value,
                                                     self.lower_lim,
                                                     self.upper_lim,
                                                     self.stepsize,
                                                     self.tolerance,
                                                     self.linkage)

#-------------------------------------------------------------------------------
