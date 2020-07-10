from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = [
    'InputFile',
]

class InputFile():

    def __init__(self, structure, filepath):
        self.name           = structure.name
        self.job_name       = structure.name
        self.filepath       = filepath

        self.parts          = self._generate_part_section(structure)
        self.assembly       = self._generate_assembly_section(structure)
        self.materials      = self._generate_material_section(structure)
        self.int_props      = self._generate_int_props_section(structure)
        self.interactions   = self._generate_interactions_section(structure)
        self.bcs            = self._generate_bcs_section(structure)
        self.steps          = self._generate_steps_section(structure)

        self.data           = self._generate_data()

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_part_section(self, structure):
        section_data = []
        for part in structure.parts:
            section_data.append(part.data)
        return ''.join(section_data)

    def _generate_assembly_section(self, structure):
        return structure.assembly.data

    def _generate_material_section(self, structure):
        section_data = []
        for material in structure.assembly.materials:
            section_data.append(material.data)
        return ''.join(section_data)

    def _generate_int_props_section(self, structure):
        # # Write interaction properties
        # for interaction_property in self.interaction_properties:
        #     interaction_property.write_data_line(f)
        return ''

    def _generate_interactions_section(self, structure):
        #
        # # Write interactions
        # for interaction in self.interactions:
        #     interaction.write_data_line(f)
        return ''

    def _generate_bcs_section(self, structure):
        section_data = []
        for bc in structure.bcs:
            section_data.append(bc.data)
        return ''.join(section_data)

    def _generate_steps_section(self, structure):
        section_data = []
        for step in structure.steps:
            section_data.append(step.data)
        return ''.join(section_data)

    def _generate_data(self):
        return """** {}
*Heading
** Job name: {}
** Generated by: compas_fea2
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
** PARTS
**
{}**
** ASSEMBLY
**
{}
**
** MATERIALS
**
{}**
** INTERACTION PROPERTIES
**
{}**
** INTERACTIONS
**
{}**
** BOUNDARY
**
{}**
** STEPS
{}
""".format(self.name, self.job_name,self.parts, self.assembly,self.materials,
           self.int_props, self.interactions, self.bcs, self.steps)

    # ==============================================================================
    # General methods
    # ==============================================================================

    def write_to_file(self):
        with open(self.filepath, 'w') as f:
            f.writelines(self.data)


if __name__ == "__main__":
    pass
