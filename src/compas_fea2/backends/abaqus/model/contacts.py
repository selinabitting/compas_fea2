from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import ContactPair


class AbaqusContactPair(ContactPair):
    def __init__(self, name, master, slave, interaction):
        super(AbaqusContactPair, self).__init__(name, master, slave, interaction)

    def _generate_jobdata(self):
        return f"""** Interaction: {self._name}
*Contact Pair, interaction={self._interaction.name}, type=SURFACE TO SURFACE
{self._master.name}, {self._slave.name}
**
"""
