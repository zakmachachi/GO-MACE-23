import random
from math import cos, pi

import numpy as np
import utilities
from ase import neighborlist


def add_edge_functionality(
    graphene,
    edge_atoms,
    h_atoms,
    funct_groups,
    distance,
    N_groups,
    funct_atoms,
    neighbor_list,
    box_size,
    max_iter,
    C_H_bond_length=1.09,
):
    # add error handling for iter > max_iter

    """
    Summary
    ----------
    Add functional group to structutre

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    edge_atoms : list
        List with indices of all edge atoms
    h_atoms : list
        Indices of h atoms in graphene structure
    funct_groups : ase.Atoms list
        List of atoms object containing possible functinal groups to be added
    distance: float
        Bond distance between group and carbon edge
    N_groups : int
        Number of functional groups to be added to surface
    funct_atoms: list
        List containing all previously oxidised H atoms
    neighbor_list: list
        List containing the atoms in the collision zone of each atom
    box_size: float
        vacuum between ribbons
    C_H_bond_length: float
        C-H bond length in (default = 1.09 A)
    max_iter: int
        Max number of iterations for rotating bond
    """

    # Copy of neighbor list - prevetns overwritting
    neighbors_cp = neighbor_list.copy()

    # Save original number of c atoms to access indices of added atoms after functionalisation
    sheet_atoms = len(graphene[graphene.numbers == 6])

    # We create a variable to keep tack of the amount of groups we have added
    N_added = 0

    # Select random hydrogens and replace them with functional groups
    for i in range(N_groups):
        # Create copy of group to prevent overwriting
        group = funct_groups[random.randint(0, len(funct_groups) - 1)].copy()

        h, funct_atoms = pick_random_h(graphene, h_atoms, funct_atoms)

        # Save position of removed h
        h_pos = np.array(graphene[h].position)

        # Orient group away from ribbon
        if h_pos[0] <= box_size / 2:
            orientation = -1
        else:
            orientation = 1
        group_pos_init = group.get_positions()
        group_pos_init *= orientation

        # Move functional group along x direction to ensure realistic bond lenght. Approx 120 degree bond angle is used for calculation
        h_pos[0] += orientation * cos((1 / 6) * pi) * (distance - C_H_bond_length)
        # Assign random initial orientation to functional group
        angle = random.uniform(0, 180)
        # Create functional group in initial position
        group = position_group(group, group_pos_init, angle, h_pos)

        # Get the collision zone of the H atom to be removed
        collision_zone = neighbors_cp[:, 1][neighbors_cp[:, 0] == h]

        valid_group = utilities.is_structure_valid(graphene, group, collision_zone)
        iter = 0
        # If group is not valid (close contacts present) then rotate it until its position is valid (oly up to max iteration times)

        while not valid_group and iter < max_iter:
            angle += random.uniform(5, 10)
            group = position_group(group, group_pos_init, angle, h_pos)
            iter += 1
            valid_group = utilities.is_structure_valid(graphene, group, collision_zone)

        # Add valid functional group to graphene sheet
        if valid_group:
            N_added += 1
            print(f"Added {N_added} edge group ({100*N_added/N_groups:.2f}%)")
            graphene.extend(group)

            for i in collision_zone:
                if i in neighbors_cp:
                    for j in range(1, len(group) + 1):
                        neighbors_cp = np.concatenate(
                            (neighbors_cp, [[i, len(graphene) - j]]), axis=0
                        )

            neighbors_cp = neighbors_cp[neighbors_cp[:, 0] != h]
            neighbors_cp = neighbors_cp[neighbors_cp[:, 1] != h]
        else:
            print("Could not add functional group to this position")
            # Remove added H from functionalised atonms
            funct_atoms = funct_atoms[funct_atoms != h]

    # Remove all unecessary H atoms
    del graphene[funct_atoms.astype(int)]

    # Save all new groups to edge atoms (All edge atoms have indices larger than the last carbon in the original sheet)
    for i in range(sheet_atoms, len(graphene)):
        edge_atoms.append(i)

    return graphene, edge_atoms, N_added


def pick_random_h(graphene, h_atoms, funct_atoms):
    """
    Summary
    ----------
    Pick a random hydrogen atom

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    h_atoms : list
        Indices of h atoms in graphene structure
    funct_atoms : list
        List of the indices of the edge hydrogen atoms which have been functionalised
    """

    # Create array of possible h atoms which can be oxidised
    choices = [h for h in h_atoms if h not in funct_atoms]

    # If choices is empty, then we have oxidised all the carbon atoms and we need to exit the function
    if len(choices) == 0:
        print(f"All edge hydrogen atoms have been oxidised")
        return None, funct_atoms
    else:
        # Choose a random H atom
        h_atom = np.random.choice(choices)
        # Append substituted H atom positions so we dont try and substitute them again
        funct_atoms = np.append(funct_atoms, h_atom)

    return h_atom, funct_atoms


def position_group(group, pos_init, angle, h_pos):
    """
    Summary
    ----------
    Add rotated functional group to ribbon

    Parameters
    ----------
    group: ase.Atoms
        Functional group added to nanoriibon
    pos_init : Positions of group if origin was (0,0,0)
        Indices of atoms that can collide with functional group
    angle:
        Angle by which to rotate group
    h_pos:
        Position of removed H atom
    """
    # Generate group centered at (0,0,0) with a random orientation
    group.set_positions(pos_init)
    group.rotate(angle, "x")

    # Connect group to graphene network
    group_pos = group.get_positions()
    group_pos += np.broadcast_to(h_pos, (len(group), 3))
    group.set_positions(group_pos)

    return group


def get_edge_carbons(graphene):
    # Build C-H NeighborList object
    i, j = neighborlist.neighbor_list(
        "i" "j", graphene, cutoff=1.15, self_interaction=False
    )
    nn_list = np.array((i, j)).T
    edge_atoms = []
    for pair in nn_list:
        if graphene[pair[0]].symbol == "H":
            # We add bot the edge C to the oxidised carbon list to avoid oxidising them again later
            edge_atoms.append(pair[1])
    return edge_atoms
