from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEABase


class BeamEndRelease(FEABase):
    """Initialises base Constraint object.
    """

    def __init__(self):
        super(BeamEndRelease, self).__init__()
