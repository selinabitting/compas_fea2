from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._core import GeneralDisplacementBase
from compas_fea2.backends._core import FixedDisplacementBase
from compas_fea2.backends._core import PinnedDisplacementBase
from compas_fea2.backends._core import FixedDisplacementXXBase
from compas_fea2.backends._core import FixedDisplacementYYBase
from compas_fea2.backends._core import FixedDisplacementZZBase
from compas_fea2.backends._core import RollerDisplacementXBase
from compas_fea2.backends._core import RollerDisplacementYBase
from compas_fea2.backends._core import RollerDisplacementZBase
from compas_fea2.backends._core import RollerDisplacementXYBase
from compas_fea2.backends._core import RollerDisplacementYZBase
from compas_fea2.backends._core import RollerDisplacementXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'GeneralDisplacement',
    'FixedDisplacement',
    'PinnedDisplacement',
    'FixedDisplacementXX',
    'FixedDisplacementYY',
    'FixedDisplacementZZ',
    'RollerDisplacementX',
    'RollerDisplacementY',
    'RollerDisplacementZ',
    'RollerDisplacementXY',
    'RollerDisplacementYZ',
    'RollerDisplacementXZ'
]


class GeneralDisplacement(GeneralDisplacementBase):
    """Initialises the base GeneralDisplacement object.

    Parameters
    ----------
    name : str
        Name of the Displacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    x : float
        Value of x translation.
    y : float
        Value of y translation.
    z : float
        Value of z translation.
    xx : float
        Value of xx rotation.
    yy : float
        Value of yy rotation.
    zz : float
        Value of zz rotation.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    nodes : str
        Node set string or nodes list the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.

    """
    pass



class FixedDisplacement(FixedDisplacementBase):
    """A fixed nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.

    """
    pass

class PinnedDisplacement(PinnedDisplacementBase):
    """A pinned nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the PinnedDisplacement object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.

    """
    pass


class FixedDisplacementXX(FixedDisplacementXXBase):
    """A pinned nodal displacement boundary condition clamped in XX.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementXX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass


class FixedDisplacementYY(FixedDisplacementYYBase):
    """A pinned nodal displacement boundary condition clamped in YY.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementYY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass


class FixedDisplacementZZ(FixedDisplacementZZBase):
    """A pinned nodal displacement boundary condition clamped in ZZ.

    Parameters
    ----------
    name : str
        Name of the FixedDisplacementZZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass


class RollerDisplacementX(RollerDisplacementXBase):
    """A pinned nodal displacement boundary condition released in X.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementX object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass

class RollerDisplacementY(RollerDisplacementYBase):
    """A pinned nodal displacement boundary condition released in Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass

class RollerDisplacementZ(RollerDisplacementZBase):
    """A pinned nodal displacement boundary condition released in Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementZ object.
    nodes : str
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass

class RollerDisplacementXY(RollerDisplacementXYBase):
    """A pinned nodal displacement boundary condition released in X and Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXY object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass

class RollerDisplacementYZ(RollerDisplacementYZBase):
    """A pinned nodal displacement boundary condition released in Y and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementYZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass

class RollerDisplacementXZ(RollerDisplacementXZBase):
    """A pinned nodal displacement boundary condition released in X and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    nodes : str, list
        Node set string or nodes list the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    """
    pass
