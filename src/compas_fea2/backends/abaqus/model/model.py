from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._base.model import ModelBase

__all__ = [
    'Model',
]


class Model(ModelBase):
    """ Abaqus Model object

    Note
    ----
    This is in many aspects equivalent to an `Assembly` in Abaqus.


    """
    __doc__ += ModelBase.__doc__

    def __init__(self, name, description=None, author=None):
        super(Model, self).__init__(name, description, author)
        self._backend = 'abaqus'


# =============================================================================
#                               Job data
# =============================================================================

    def _generate_jobdata(self):
        return f"""**
** PARTS
**
{self._generate_part_section()}**
** MATERIALS
**
{self._generate_material_section()}**
** INTERACTION PROPERTIES
**
{self._generate_int_props_section()}**
** INTERACTIONS
**
{self._generate_interactions_section()}**
** ASSEMBLY
**
{self._generate_assembly_section()}**
** BOUNDARY CONDITIONS
**
{self._generate_bcs_section()}**
"""

    def _generate_part_section(self):
        """Generate the content relatitive the each Part for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for part in self.parts.values():
            data = part._generate_jobdata()
            section_data.append(data)
        return ''.join(section_data)

    def _generate_assembly_section(self):
        """Generate the content relatitive the assembly for the input file.

        Note
        ----
        in compas_fea2 the Model is for many aspects equivalent to an assembly in
        abaqus.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = ['*Assembly, name={}\n**\n'.format(self.name)]
        for instance in self.instances.values():
            section_data.append(instance._generate_jobdata())
            for group in instance.groups.values():
                section_data.append(group._generate_jobdata())
            # for surface in self.surfaces:
            #     section_data.append(surface.jobdata)
        for constraint in self.constraints.values():
            section_data.append(constraint._generate_jobdata())
        section_data.append('*End Assembly\n**\n')

        return ''.join(section_data)

    def _generate_material_section(self):
        """Generate the content relatitive to the material section for the input
        file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for material in self.materials.values():
            section_data.append(material._generate_jobdata())
        return ''.join(section_data)

    def _generate_int_props_section(self):
        return ''

    def _generate_interactions_section(self):
        return ''

    def _generate_bcs_section(self):
        """Generate the content relatitive to the boundary conditions section
        for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        section_data = []
        for bc in self.bcs.values():
            section_data.append(bc._generate_jobdata())
        return ''.join(section_data)


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
