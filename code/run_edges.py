# main_script.py

import time
from math import cos, pi, sin

import numpy as np
from ase import Atoms
from ase.build import graphene_nanoribbon
from ase.io import read, write
from generate_GO import build


# Define a function to run the functionalization process
def run_functionalization(
    input_structure,
    O_content,
    OH_ratio,
    disorder,
    p6,
    edges,
    p4,
    funct_groups,
    vacuum,
    max_iterations,
    output_structure,
):
    start_time = time.time()

    # Create an instance of the build class
    build_instance = build()

    # Call the main function from the build class
    build_instance.main(
        input_structure,
        O_content,
        OH_ratio,
        disorder,
        p6,
        edges,
        p4,
        funct_groups,
        vacuum,
        max_iterations,
        output_structure,
    )


# Is the structure disordered?
disorder = False

# Are the edges functionalized?
edges = True

# Enter range of O_content, OH_fraction and p6 values to be used
# O_content_range = np.arange(0.1, 0.6, 0.1)
O_content_range = [0.3]
OH_fraction_range = np.arange(0.0, 1.25, 0.25)
# OH_fraction_range = [0.5]
if disorder:
    p6_range = [0.7]
    p6_range = np.arange(0.3, 0.8, 0.1)
else:
    p6_range = [1]
if edges:
    # p4_range = [1]
    p4_range = np.arange(0.1, 0.6, 0.1)
else:
    p4_range = [0]


# Generate carboxyl group centered at (0,0,0)
carboxyl = Atoms("COOH", positions=[(0, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0)])
carboxyl.set_positions(
    [
        (0, 0, 0),
        (sin(5 * pi / 6) * 1.21, 0, cos(5 * pi / 6) * 1.21),
        (sin(pi / 6) * 1.30, 0, cos(pi / 6) * 1.30),
        (
            sin(pi / 6) * 1.30 + sin(pi / 2) * 0.96,
            0,
            cos(pi / 6) * 1.30 + cos(pi / 2) * 0.96,
        ),
    ]
)
# Generate aldehyde group centered at (0,0,0) - approx bond angle 120
aldehyde = Atoms("CHO", positions=[(0, 0, 0), (0, 1, 0), (0, 0, 1)])
aldehyde.set_positions(
    [
        (0, 0, 0),
        (sin(5 * pi / 6) * 1.09, 0, cos(5 * pi / 6) * 1.09),
        (sin(pi / 6) * 1.20, 0, cos(pi / 6) * 1.20),
    ]
)
# Generate OH group centered at (0,0,0)
hydroxyl = Atoms("OH", positions=[(0, 0, 0), (0, 1, 0)])
hydroxyl.set_positions([(0, 0, 0), (sin(pi / 6) * 0.96, 0, cos(pi / 6) * 0.96)])

# Tuple containing the functional groups for edge functionalisation
funct_groups = (carboxyl, aldehyde, hydroxyl)

# Store value of vacuum along direction of edges
vacuum = 10

if disorder:
    # Path to input structure
    input_strucuture = "../structures/aG_p6.xyz"
    print("Reading amorphous database")
    graphene = read(input_strucuture, index=":")
    graphene_init = graphene.copy()

elif edges:
    # Create saturated 1D ribbon
    graphene_init = graphene_nanoribbon(
        7, 5, type="armchair", saturated=True, sheet=False, vacuum=vacuum
    )

else:
    # Create pristine 2D graphene
    graphene_init = graphene_nanoribbon(
        7, 5, type="armchair", saturated=False, sheet=True, vacuum=vacuum
    )

for j in range(20):
    for O_content in O_content_range:
        for OH_fraction in OH_fraction_range:
            for p6 in p6_range:
                for p4 in p4_range:
                    if not disorder:
                        # We need a copy of initial structure to avoid oxidising the same strucuture twice.
                        graphene = graphene_init.copy()
                    # Define the output structure name
                    output_structure = f"../inital_configs/p2-p3/batch-{j}/GO-{OH_fraction:.2f}-{p4:.2f}.xyz".format(
                        O_content, p4
                    )
                    # Run the functionalization process
                    run_functionalization(
                        graphene,
                        O_content,
                        OH_fraction,
                        disorder,
                        p6,
                        edges,
                        p4,
                        funct_groups,
                        vacuum,
                        200,
                        output_structure,
                    )
