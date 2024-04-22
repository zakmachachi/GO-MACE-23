import math

import numpy as np


# check if this is needed or not
def minimum_image(vector, box_size):
    # Apply the periodic boundary conditions to the vector
    for i in range(3):
        if abs(vector[i]) > box_size[i] / 2:
            vector[i] -= box_size[i] * round(vector[i] / box_size[i])
    return vector


def is_structure_valid(
    graphene, group, collision_zone, r_c=1.85 / 2, r_o=1.52 / 2, r_h=1.2 / 2
):
    """
    Summary
    ----------
    Check if functional group can be added to graphene sheet without causing close contacts

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    group: ase.Atoms
        Functional group added to nanoriibon; Atom attached to ribbon must be placed at (0,0,0)
    collision_zone : list
        Indices of atoms that can collide with functional group
    r_c:
        Hard sphere radius for carbon (Default value is VdW radius)
    r_o:
        Hard sphere radius for oxygen (Default value is VdW radius)
    r_h:
        Hard sphere radius for hydrogen (Default value is VdW radius)
    """
    # Cut offs for checking for collisions
    threshholds = {
        "CC": r_c * 2,
        "OO": r_o * 2,
        "HH": r_h * 2,
        "HC": r_c + r_h,
        "CH": r_c + r_h,
        "OH": r_o + r_h,
        "HO": r_o + r_h,
        "CO": r_c + r_o,
        "OC": r_c + r_o,
    }
    # If collision zone is empty then structure is valid
    if len(collision_zone) == 0:
        return True

    # Loop over pairs to check for collisions
    for atom in group:
        for i in collision_zone:
            pair = graphene[i].symbol + atom.symbol
            atom_1 = np.array(graphene[i].position)
            atom_2 = np.array(atom.position)
            # Apply minimum image convention
            dx = abs(atom_1[0] - atom_2[0])
            dx = min(dx, graphene.get_cell()[0, 0] - dx)
            dy = abs(atom_1[1] - atom_2[1])
            dy = min(dy, graphene.get_cell()[1, 1] - dy)
            dz = abs(atom_1[2] - atom_2[2])
            dz = min(dz, graphene.get_cell()[2, 2] - dz)

            # Calculate distance between atoms
            min_dist = math.sqrt(dx**2 + dy**2 + dz**2)

            # Check min distance
            if min_dist <= threshholds[pair]:
                return False
    return True
