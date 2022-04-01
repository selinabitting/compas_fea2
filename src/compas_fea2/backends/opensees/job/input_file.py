import os.path
from datetime import datetime
from compas_fea2.job.input_file import InputFile

from ..problem.steps import OpenseesModalStep


class OpenseesInputFile(InputFile):
    """Input file object for standard analysis.

    Parameters
    ----------
    problem : obj
        Problem object.

    Attributes
    ----------
    name : str
        Input file name.
    job_name : str
        Name of the Abaqus job. This is the same as the input file name.
    data : str
        Final input file text data that will be written in the .tcl file.
    """

    def __init__(self, name=None, **kwargs):
        super(OpenseesInputFile, self).__init__(name=name, **kwargs)
        self._extension = 'tcl'

    def _generate_jobdata(self, problem):
        """Generate the content of the input fileself from the Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Return
        ------
        str
            content of the input file
        """
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"""# ------------------------
# {problem.model.name}
# ------------------------
#
# {problem.model.description}
#
# Units: kips, in, sec CHANGE
#
# Author:None CHANGE
# Date: {now}
# Generated by: compas_fea2
#
#------------------------------------------------------------------
#------------------------------------------------------------------
# MODEL
#------------------------------------------------------------------
#------------------------------------------------------------------
#
#{problem.model._generate_jobdata()}
#
#
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# PROBLEM
# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
#
{problem}
#
#------------------------------------------------------------------
#------------------------------------------------------------------
# Solver
#------------------------------------------------------------------
#------------------------------------------------------------------
#
# initialize Model in case an initial stiffness iteration is required
initialize
#
# Create the system of equation
system ProfileSPD
#
# Create the constraint handler, the transformation method
constraints Transformation
#
# Create the DOF numberer, the reverse Cuthill-McKee algorithm
numberer RCM
#
# Create the convergence test
test NormUnbalance {problem.tolerance} {problem.iterations} 5'
#
# Create the solution algorithm, a Newton-Raphson algorithm
algorithm NewtonLineSearch
#
# Create the integration scheme, the LoadControl scheme using steps of 0.1
integrator LoadControl {problem.increments}
#
# Create the analysis object
analysis Static


# ------------------------------
# Start of recorder generation
# ------------------------------

# Create a recorder to monitor nodal displacements
recorder Node -xml nodeGravity.out -time -node 3 4 -dof 1 2 3 disp

# --------------------------------
# End of recorder generation
# ---------------------------------


# ------------------------------
# Finally perform the analysis
# ------------------------------

# perform the gravity load analysis, requires 10 steps to reach the load level
analyze 10

puts "Node 3 after Gravity Analysis:"
print node 3

remove recorders
#
# Output
#-------
#
{problem}
#
# Solver
#-------
#
#
{problem}
"""
# """.format(self.name, self.job_name, self._generate_part_section(problem), self._generate_assembly_section(problem),
#            self._generate_material_section(problem), self._generate_int_props_section(problem),
#            self._generate_interactions_section(problem), self._generate_bcs_section(problem),
#            self._generate_steps_section(problem))

    def _generate_part_section(self, problem):
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
        for part in problem.model.parts.values():
            data = part._generate_jobdata()
            section_data.append(data)
        return ''.join(section_data)

    def _generate_assembly_section(self, problem):
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
        return problem.model._generate_jobdata()

    def _generate_material_section(self, problem):
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
        for material in problem.model.materials.values():
            section_data.append(material.jobdata)
        return ''.join(section_data)

    def _generate_int_props_section(self, problem):
        # # Write interaction properties
        # for interaction_property in problem.model.interaction_properties:
        #     interaction_property.write_data_line(f)
        return ''

    def _generate_interactions_section(self, problem):
        #
        # # Write interactions
        # for interaction in problem.model.interactions:
        #     interaction.write_data_line(f)
        return ''

    def _generate_bcs_section(self, problem):
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
        for bc in problem.bcs.values():
            section_data.append(bc._generate_jobdata())
        return ''.join(section_data)

    def _generate_steps_section(self, problem):
        """Generate the content relatitive to the steps section for the input
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
        for step in problem.steps:
            if isinstance(step, OpenseesModalStep):  # TODO too messy - check!
                section_data.append(step._generate_jobdata())
            else:
                section_data.append(step._generate_jobdata(problem))

        return ''.join(section_data)
