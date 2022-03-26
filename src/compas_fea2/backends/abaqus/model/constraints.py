from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import TieConstraint


class AbaqusTieConstraint(TieConstraint):

    def __init__(self, name, master, slave):
        super(AbaqusTieConstraint, self).__init__(name, master, slave, tol=None)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        return ''.join([
            f'** Constraint: {self.name}\n',
            '*MPC\n',
            f'TIE, {self.slave}, {self.master}\n'
        ])
