from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class FieldOutput(FEAData):
    """FieldOutput object for specification of the fields (stresses, displacements,
    etc..) to output from the analysis.

    Parameters
    ----------
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    Attributes
    ----------
    name : str
        Automatically generated id. You can change the name if you want a more
        human readable input file.
    nodes_outputs : list
        list of node fields to output
    elements_outputs : list
        list of elements fields to output

    """

    def __init__(self, node_outputs, element_outputs):
        super(FieldOutput, self).__init__()
        self._name = id(self)
        self._node_outputs = node_outputs
        self._element_outputs = element_outputs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def node_outputs(self):
        """list : list of node fields to output."""
        return self._node_outputs

    @property
    def element_outputs(self):
        """list : list of elements fields to output."""
        return self._element_outputs


class HistoryOutput(FEAData):
    """HistoryOutput object for recording the fields (stresses, displacements,
    etc..) from the analysis.

    Parameters
    ----------
    name : str
        name of the output request
    """

    def __init__(self, name):
        super(HistoryOutput, self).__init__()
        self.__name__ = 'HistoryOutputRequst'
        self._name = name

    @property
    def name(self):
        """str : name of the output request"""
        return self._name
