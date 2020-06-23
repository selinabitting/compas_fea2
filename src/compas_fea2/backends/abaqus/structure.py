from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

# from compas_fea.utilities import combine_all_sets
# from compas_fea2.utilities import group_keys_by_attribute
# from compas_fea2.utilities import group_keys_by_attributes

from compas_fea2.backends._core import StructureBase

# from compas_fea2.backends.abaqus.components import Set
# from compas_fea2.backends.abaqus.components.elements import *

from compas_fea2.backends.abaqus.writer import InputFile

from compas_fea2.backends.abaqus.job.send_job import launch_process
from compas_fea2.backends.abaqus.job.read_results import extract_data

# from compas_fea2.backends.abaqus.writer import Writer

# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'Structure',
]

class Structure(StructureBase):

    def __init__(self, name, parts, assembly, interactions, bcs, steps):
        super(Structure, self).__init__(name=name)
        self.parts = parts
        self.assembly = assembly
        self.interactions = interactions
        self.bcs = bcs
        self.steps = steps


    def write_input_file(self, fields='u', output=True, save=False, path='C:/'):
        """Writes abaqus input file.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        output : bool
            Print terminal output.
        save : bool
            Save structure to .cfea before file writing.

        Returns
        -------
        None

        """
        # directory='{0}'.format(self.path, self.name)
        filename = '{0}/{1}.inp'.format(path, self.name)

        if not os.path.exists(path):
            os.makedirs(path)
        if save:
            self.save_to_cfea()

        # if isinstance(fields, str):
        #     fields = [fields]

        # if 'u' not in fields:
        #     fields.append('u')


        input_file = InputFile(self, filename)
        input_file.write_to_file()
        if output:
            print('***** Abaqus input file generated: {0} *****\n'.format(filename))

        # # Open input file
        # f=open(self.path,'w')

        # # write heading
        # self.write_heading(self.name, self.job_name, f)
        # # Write parts
        # for part in self.parts:
        #     part.write_keyword_start(f)
        #     part.write_data(f)
        #     part.write_keyword_end(f)

        # # Write Assembly
        # self.assembly.write_keyword_start(f)
        # # Write instances
        # for instance in self.assembly.instances:
        #     instance.write_data_line(f)
        # # Write assembly node sets
        # for nset in self.assembly.nsets:
        #     nset.write_data_line(f)
        # # Write assembly element sets
        # for elset in self.assembly.elsets:
        #     elset.write_data_line(f)
        # # Write assembly surfaces
        # for surface in self.assembly.surfaces:
        #     surface.write_data_line(f)
        # for constraint in self.assembly.constraints:
        #     constraint.write_data_line(f)
        # self.assembly.write_keyword_end(f)

        # # Write materials
        # for material in self.assembly.materials:
        #     material.write_data_line(f)

        # # # Write interaction properties
        # # for interaction_property in self.interaction_properties:
        # #     interaction_property.write_data_line(f)
        # #
        # # # Write interactions
        # # for interaction in self.interactions:
        # #     interaction.write_data_line(f)

        # # Write boundary conditions
        # for bc in self.bcs:
        #     bc.write_data(f)

        # # Write steps
        # for step in self.steps:
        #     step.write_header(f)
        #     # Write loads
        #     for load in self.loads[step]:
        #         load.write_data_line(f)
        #     # Write Output Reequests
        #     for output in self.outputs[step]:
        #         output.write_data_line(f)
        #     step.write_keyword_end(f)

        # # Close input file
        # f.close()

    # this should be an abstract method of the base class
    def analyse(self, fields='u', exe=None, cpus=4, license='research', delete=True, output=True, overwrite=True, user_mat=False, save=False):
        """Runs the analysis through abaqus.

        Parameters
        ----------

        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        delete : bool
            -
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """
        self.write_input_file(fields=fields, output=output, save=save)

        cpus = 1 if license == 'student' else cpus
        launch_process(self, exe=exe, cpus=cpus, output=output, overwrite=overwrite, user_mat=user_mat)

    # this should be an abstract method of the base class
    def extract(self, fields='u', steps='all', exe=None, sets=None, license='research', output=True,
                     return_data=True, components=None):
        """Extracts data from the analysis output files.

        Parameters
        ----------
        software : str
            Analysis software / library to use, 'abaqus', 'opensees' or 'ansys'.
        fields : list, str
            Data field requests.
        steps : list
            Loads steps to extract from.
        exe : str
            Full terminal command to bypass subprocess defaults.
        sets : list
            -
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.

        Returns
        -------
        None

        """
        extract_data(self, fields=fields, exe=exe, output=output, return_data=return_data,
                            components=components)

    # this should be an abstract method of the base class
    def analyse_and_extract(self, fields='u', exe=None, cpus=4, license='research', output=True, save=False,
                            return_data=True, components=None, user_mat=False, overwrite=True):
        """Runs the analysis through the chosen FEA software / library and extracts data.

        Parameters
        ----------
        fields : list, str
            Data field requests.
        exe : str
            Full terminal command to bypass subprocess defaults.
        cpus : int
            Number of CPU cores to use.
        license : str
            Software license type: 'research', 'student'.
        output : bool
            Print terminal output.
        save : bool
            Save the structure to .obj before writing.
        return_data : bool
            Return data back into structure.results.
        components : list
            Specific components to extract from the fields data.
        user_sub : bool
            Specify the user subroutine if needed.

        Returns
        -------
        None

        """

        self.analyse(exe=exe, fields=fields, cpus=cpus, license=license, output=output, user_mat=user_mat, overwrite=overwrite, save=save)

        self.extract(fields=fields, exe=exe, license=license, output=output,
                          return_data=return_data, components=components)


    # ==============================================================================
    # Results
    # ==============================================================================

    # this should be stored in a more generic way
    def get_nodal_results(self, step, field, nodes='all'):
        """Extract nodal results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        nodes : str, list
            Extract 'all' or a node set/list.

        Returns
        -------
        dict
            The nodal results for the requested field.
        """
        data  = {}
        rdict = self.results[step]['nodal']

        if nodes == 'all':
            keys = list(self.nodes.keys())
        elif isinstance(nodes, str):
            keys = self.sets[nodes].selection
        else:
            keys = nodes

        for key in keys:
            data[key] = rdict[field][key]

        return data


    def get_element_results(self, step, field, elements='all'):
        """Extract element results from self.results.

        Parameters
        ----------
        step : str
            Step to extract from.
        field : str
            Data field request.
        elements : str, list
            Extract 'all' or an element set/list.

        Returns
        -------
        dict
            The element results for the requested field.

        """
        data  = {}
        rdict = self.results[step]['element']

        if elements == 'all':
            keys = list(self.elements.keys())
        elif isinstance(elements, str):
            keys = self.sets[elements].selection
        else:
            keys = elements

        for key in keys:
            data[key] = rdict[field][key]

        return data