from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Constraint(FEAData):
    """Initialises base Constraint object.

    Parameters
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, *, master, slave, tol, **kwargs):
        super(Constraint, self).__init__(**kwargs)
        self._master = master
        self._slave = slave
        self._tol = tol

    @property
    def master(self):
        return self._master

    @property
    def slave(self):
        return self._slave

    @property
    def tol(self):
        return self._tol


class TieConstraint(Constraint):
    """Tie constraint between two sets of nodes, elements or surfaces.

    Parameters
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """

    def __init__(self, *, master, slave, tol, **kwargs):
        super(TieConstraint, self).__init__(master, slave, tol, **kwargs)


class Pin3DConstraint(Constraint):
    """Pin constraint between two sets of nodes, elements or surfaces that allows
    all rotations and fixes all translations.

    Parameters
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    Attributes
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.

    """
    pass


class Pin2DConstraint(Constraint):
    """Pin constraint between two sets of nodes, elements or surfaces that allows
    rotations about an axis and fixes all translations.

    Parameters
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.
    axis : :class:`compas.geometry.Vector`
        Axis of rotation.

    Attributes
    ----------
    master : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as master.
    slave : :class:`compas_fea2.model.NodesGroup`
        Goup of nodes that act as slave.
    tol : float
        Constraint tolerance, distance limit between master and slave.
    axis : :class:`compas.geometry.Vector`
        Axis of rotation.

    """

    def __init__(self, *, master, slave, tol, axis, **kwargs):
        super(SliderConstraint, self).__init__(master, slave, tol, **kwargs)
        self.axis = axis


class SliderConstraint(Constraint):

    def __init__(self, *, master, slave, tol, plane, **kwargs):
        super(SliderConstraint, self).__init__(master, slave, tol, **kwargs)
        self.plane = plane
