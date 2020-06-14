"""
********************************************************************************
Utilities
********************************************************************************

.. currentmodule:: compas_fea.utilities


Functions
=========

.. autosummary::
    :toctree: generated/

    colorbar
    combine_all_sets
    group_keys_by_attribute
    group_keys_by_attributes
    identify_ranges
    mesh_from_shell_elements
    network_order
    normalise_data
    principal_stresses
    process_data
    postprocess
    plotvoxels


"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .functions import *

__all__ = [name for name in dir() if not name.startswith('_')]
