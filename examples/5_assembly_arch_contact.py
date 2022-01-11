from itertools import tee
from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus.model.interactions import ContactHardFrictionPenalty
from compas_fea2.backends.abaqus.model.surfaces import Surface
from compas_fea2.backends.abaqus.model.contacts import ContactPair
from compas_fea2.backends.abaqus.model.elements import SolidElement

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

from compas_fea2.backends.abaqus import Results

from pathlib import Path
from compas_fea2 import TEMP

import numpy as np
import scipy.interpolate


def define_arch(n=5):
    cp_out = np.array([[0, 0], [2.5, 3.5], [5, 5], [7.5, 3.5], [10, 0]])
    cp_in = np.array([[0.5, 0], [2.2, 2.5], [5, 4.5], [7.8, 2.5], [9.5, 0]])
    cps = [cp_out, cp_in]

    curves = []
    for ly in [0, 1]:
        for cp in cps:
            curve = scipy.interpolate.interp1d(cp[:, 0], cp[:, 1], kind='quadratic')
            x = np.linspace(np.min(cp[:, 0]), np.max(cp[:, 0]), n)
            y = np.ones_like(x)*ly
            z = curve(x)
            curves.append(np.vstack([x, y, z]).T)

    return curves


##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')
# Define materials
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)
# Define sections
sec = SolidSection(name='sec_A', material=mat)

n = 9
curves = define_arch(n+1)
for i in range(len(curves[0])-1):
    block = Part(name=f'block-{i}')
    block.add_nodes([Node(curves[0][i]),
                     Node(curves[1][i]),
                     Node(curves[3][i]),
                     Node(curves[2][i]),
                     Node(curves[0][i+1]),
                     Node(curves[1][i+1]),
                     Node(curves[3][i+1]),
                     Node(curves[2][i+1])
                     ])
    block.add_element(SolidElement([0, 1, 2, 3, 4, 5, 6, 7], sec))
    # Add a Part to the model
    model.add_part(block)

# Assign boundary conditions
model.add_fix_bc(name='left_support', part='block-0', nodes=[0, 1, 2, 3])
model.add_fix_bc(name='right_support', part=f'block-{n-1}', nodes=[4, 5, 6, 7])

master, slave = tee(model.parts.keys())
next(slave, None)

for m, s in zip(master, slave):
    if s:
        model.add_contact(ContactPair(name=f'CP_{m[-1]}-{s[-1]}',
                                      master=Surface(f'{m}_S2', m, 1, 'S2'),
                                      slave=Surface(f'{s}_S1', s, 1, 'S1'),
                                      interaction=ContactHardFrictionPenalty('hard_contact', 0.2)))

# Review
# model.summary()
# model.show(scale_factor=0.1)


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='arch_hard_contact', model=model)

# Approach 1: Create a step and assign a gravity load
step_0 = GeneralStaticStep(name='step_0')
step_0.add_gravity_load()
problem.add_step(step_0)

# Define the field outputs required
fout = FieldOutput(name='fout')
problem.add_output(fout, 'step_0')

# Review
# problem.summary()
# problem.show(scale_factor=0.1)

# Solve the problem
problem.analyse(path=Path(TEMP).joinpath(problem.name))
