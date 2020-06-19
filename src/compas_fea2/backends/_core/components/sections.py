
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'SectionBase',
    'AngleSectionBase',
    'BoxSectionBase',
    'CircularSectionBase',
    'GeneralSectionBase',
    'ISectionBase',
    'PipeSectionBase',
    'RectangularSectionBase',
    'ShellSectionBase',
    'MembraneSectionBase',
    'SolidSectionBase',
    'TrapezoidalSectionBase',
    'TrussSectionBase',
    'StrutSectionBase',
    'TieSectionBase',
    'SpringSectionBase',
    'MassSectionBase'
]


class SectionBase(object):
    """Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.

    Attributes
    ----------
    name : str
        Section object name.
    geometry : dict
        Geometry of the Section.

    """

    def __init__(self, name, material):

        self.__name__ = 'Section'
        self.name     = name
        self.material = material
        self.geometry = {}

    def __str__(self):
        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))
        print('name  : {0}'.format(self.name))
        for i, j in self.geometry.items():
            print('{0:<5} : {1}'.format(i, j))
        return ''

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)


# ==============================================================================
# 0D
# ==============================================================================

class MassSectionBase(SectionBase):
    """Section for mass elements.

    Parameters
    ----------
    name : str
        Section name.

    """

    def __init__(self, name):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'MassSection'
        self.name     = name
        self.geometry = None


# ==============================================================================
# 1D
# ==============================================================================

class AngleSectionBase(SectionBase):
    """Uniform thickness angle cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    t : float
        Thickness.

    Notes
    -----
    - Ixy not yet calculated.

    """

    def __init__(self, name, b, h, t, material):
        SectionBase.__init__(self, name=name, material=material)

        p   = 2. * (b + h - t)
        xc  = (b**2 + h * t - t**2) / p
        yc  = (h**2 + b * t - t**2) / p
        A   = t * (b + h - t)
        Ixx = (1. / 3) * (b * h**3 - (b - t) * (h - t)**3) - A * (h - yc)**2
        Iyy = (1. / 3) * (h * b**3 - (h - t) * (b - t)**3) - A * (b - xc)**2
        J   = (1. / 3) * (h + b - t) * t**3

        self.__name__ = 'AngleSection'
        # self.name     = name
        self.geometry = {'b': b, 'h': h, 't': t, 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': None}


class BoxSectionBase(SectionBase):
    """Hollow rectangular box cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.

    """

    def __init__(self, name, b, h, tw, tf, material):
        SectionBase.__init__(self, name=name, material=material)

        A   = b * h - (b - 2 * tw) * (h - 2 * tf)
        Ap  = (h - tf) * (b - tw)
        Ixx = (b * h**3) / 12. - ((b - 2 * tw) * (h - 2 * tf)**3) / 12.
        Iyy = (h * b**3) / 12. - ((h - 2 * tf) * (b - 2 * tw)**3) / 12.
        p   = 2 * ((h - tf) / tw + (b - tw) / tf)
        J   = 4 * (Ap**2) / p

        self.__name__ = 'BoxSection'
        self.name     = name
        self.geometry = {'b': b, 'h': h, 'tw': tw, 'tf': tf, 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0}


class CircularSectionBase(SectionBase):
    """Solid circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Radius.

    """

    def __init__(self, name, r):
        SectionBase.__init__(self, name=name)

        D   = 2 * r
        A   = 0.25 * pi * D**2
        Ixx = Iyy = (pi * D**4) / 64.
        J   = (pi * D**4) / 32

        self.__name__ = 'CircularSection'
        self.name     = name
        self.geometry = {'r': r, 'D': D, 'A': A, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0, 'J': J}


class GeneralSectionBase(SectionBase):
    """General cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.
    Ixx : float
        Second moment of area about axis x-x.
    Ixy : float
        Cross moment of area.
    Iyy : float
        Second moment of area about axis y-y.
    J : float
        Torsional rigidity.
    g0 : float
        Sectorial moment.
    gw : float
        Warping constant.

    """

    def __init__(self, name, A, Ixx, Ixy, Iyy, J, g0, gw):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'GeneralSection'
        self.name     = name
        self.geometry = {'A': A, 'Ixx': Ixx, 'Ixy': Ixy, 'Iyy': Iyy, 'J': J, 'g0': g0, 'gw': gw}


class ISectionBase(SectionBase):
    """Equal flanged I-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.
    tw : float
        Web thickness.
    tf : float
        Flange thickness.

    """

    def __init__(self, name, b, h, tw, tf):
        SectionBase.__init__(self, name=name)

        A   = 2 * b * tf + (h - 2 * tf) * tw
        Ixx = (tw * (h - 2 * tf)**3) / 12. + 2 * ((tf**3) * b / 12. + b * tf * (h / 2. - tf / 2.)**2)
        Iyy = ((h - 2 * tf) * tw**3) / 12. + 2 * ((b**3) * tf / 12.)
        J   = (1. / 3) * (2 * b * tf**3 + (h - tf) * tw**3)

        self.__name__ = 'ISection'
        self.name     = name
        self.geometry = {'b': b, 'h': h, 'tw': tw, 'tf': tf, 'c': h/2., 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0}


class PipeSectionBase(SectionBase):
    """Hollow circular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    r : float
        Outer radius.
    t : float
        Wall thickness.

    """

    def __init__(self, name, r, t):
        SectionBase.__init__(self, name=name)

        D   = 2 * r
        A   = 0.25 * pi * (D**2 - (D - 2 * t)**2)
        Ixx = Iyy = 0.25 * pi * (r**4 - (r - t)**4)
        J   = (2. / 3) * pi * (r + 0.5 * t) * t**3

        self.__name__ = 'PipeSection'
        self.name     = name
        self.geometry = {'r': r, 't': t, 'D': D, 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0}


class RectangularSectionBase(SectionBase):
    """Solid rectangular cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b : float
        Width.
    h : float
        Height.

    """

    def __init__(self, name, b, h):
        SectionBase.__init__(self, name=name)

        A   = b * h
        Ixx = (1 / 12.) * b * h**3
        Iyy = (1 / 12.) * h * b**3
        l1  = max([b, h])
        l2  = min([b, h])
        # Avy = 0.833 * A
        # Avx = 0.833 * A
        J   = (l1 * l2**3) * (0.33333 - 0.21 * (l2 / l1) * (1 - (l2**4) / (12 * l1**4)))

        self.__name__ = 'RectangularSection'
        self.name     = name
        self.geometry = {'b': b, 'h': h, 'A': A, 'J': J, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0}


class TrapezoidalSectionBase(SectionBase):
    """Solid trapezoidal cross-section for beam elements.

    Parameters
    ----------
    name : str
        Section name.
    b1 : float
        Width at bottom.
    b2 : float
        Width at top.
    h : float
        Height.

    Notes
    -----
    - J not yet calculated.

    """

    def __init__(self, name, b1, b2, h):
        SectionBase.__init__(self, name=name)

        c   = (h * (2 * b2 + b1)) / (3. * (b1 + b2))
        A   = 0.5 * (b1 + b2) * h
        Ixx = (1 / 12.) * (3 * b2 + b1) * h**3
        Iyy = (1 / 48.) * h * (b1 + b2) * (b2**2 + 7 * b1**2)

        self.__name__ = 'TrapezoidalSection'
        self.name     = name
        self.geometry = {'b1': b1, 'b2': b2, 'h': h, 'A': A, 'c': c, 'Ixx': Ixx, 'Iyy': Iyy, 'Ixy': 0, 'J': None}


class TrussSectionBase(SectionBase):
    """For use with truss elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'TrussSection'
        self.name     = name
        self.geometry = {'A': A, 'Ixx': 0, 'Iyy': 0, 'Ixy': 0, 'J': 0}


class StrutSectionBase(TrussSectionBase):
    """For use with strut elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        TrussSectionBase.__init__(self, name=name, A=A)

        self.__name__ = 'StrutSection'


class TieSectionBase(TrussSectionBase):
    """For use with tie elements.

    Parameters
    ----------
    name : str
        Section name.
    A : float
        Area.

    """

    def __init__(self, name, A):
        TrussSectionBase.__init__(self, name=name, A=A)

        self.__name__ = 'TieSection'


class SpringSectionBase(SectionBase):
    """For use with spring elements.

    Parameters
    ----------
    name : str
        Section name.
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Notes
    -----
    - Force and displacement data should range from negative to positive values.
    - Requires either a stiffness dict for linear springs, or forces and displacement lists for non-linear springs.
    - Directions are 'axial', 'lateral', 'rotation'.

    """

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        SectionBase.__init__(self, name=name)

        self.__name__      = 'SpringSection'
        self.name          = name
        self.geometry      = None
        self.forces        = forces
        self.displacements = displacements
        self.stiffness     = stiffness


# ==============================================================================
# 2D
# ==============================================================================

class ShellSectionBase(SectionBase):
    """Section for shell elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.

    """

    def __init__(self, name, t):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'ShellSection'
        self.name     = name
        self.geometry = {'t': t}


class MembraneSectionBase(SectionBase):
    """Section for membrane elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.

    """

    def __init__(self, name, t):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'MembraneSection'
        self.name     = name
        self.geometry = {'t': t}


# ==============================================================================
# 3D
# ==============================================================================

class SolidSectionBase(SectionBase):
    """Section for solid elements.

    Parameters
    ----------
    name : str
        Section name.

    """

    def __init__(self, name):
        SectionBase.__init__(self, name=name)

        self.__name__ = 'SolidSection'
        self.name     = name
        self.geometry = None



