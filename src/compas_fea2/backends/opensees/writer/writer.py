
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends.opensees.writer import Heading
from compas_fea2.backends.opensees.writer.elements import Elements
from compas_fea2.backends.opensees.writer.elements import Nodes
from compas_fea2.backends.opensees.writer.bcs import BCs
from compas_fea2.backends.opensees.writer.materials import Materials
from compas_fea2.backends.opensees.writer.steps import Steps


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Writer',
]


class Writer(Steps, Materials, BCs, Elements, Nodes, Heading):

    """ Initialises base file writer.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """

    def __init__(self, structure, filename, fields, ndof=6):

        self.comment   = '#' #TODO I can bring the writer in utilities and just change these characters
        self.filename  = filename
        self.ndof      = ndof
        self.structure = structure
        self.fields    = fields
        self.spacer    = ' '

        #TODO check if it is possible to collecte all the tags here

    def __enter__(self):

        self.file = open(self.filename, 'w')
        return self


    def __exit__(self, type, value, traceback):

        self.file.close()


    def blank_line(self):

        self.file.write('{0}\n'.format(self.comment))


    def divider_line(self):

        self.file.write('{0}------------------------------------------------------------------\n'.format(self.comment))


    def write_line(self, line):

        self.file.write('{0}\n'.format(line))


    def write_section(self, section):

        self.divider_line()
        self.write_line('{0} {1}'.format(self.comment, section))
        self.divider_line()


    def write_subsection(self, subsection):

        self.write_line('{0} {1}'.format(self.comment, subsection))
        self.write_line('{0}-{1}'.format(self.comment, '-' * len(subsection)))
        self.blank_line()