import numpy as np
import utilities
from ase import Atom, neighborlist


def select_disordered(p6, graphene):
    # Given a p6 value, we need to select a structure which has the closest p6 value to the desired value.
    # We need to incorporate some variance so we need to bin the p6 values and select a random structure from the bin.

    p6_store = np.array([atom.info["p6"] for atom in graphene])
    hist, bin_edges = np.histogram(p6_store, bins=100)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Find the bin index with the closest p6 value to the desired value
    bin_index = np.argmin(abs(bin_centers - p6))

    # Get all the structures falling in the selected bin
    structures_in_bin = [
        graphene[i]
        for i in range(len(graphene))
        if bin_edges[bin_index] <= p6_store[i] < bin_edges[bin_index + 1]
    ]
    # If there are no structures in the selected bin, return None or raise an exception
    if not structures_in_bin:
        # print(structures_in_bin)
        raise ValueError("No structures found in the selected bin.")
        # or you can return None or any other value to indicate that no structure was found
    # If there are multiple structures with the same p6 value within the selected bin, randomly choose one
    selected_index = np.random.randint(0, len(structures_in_bin))
    selected_structure = structures_in_bin[selected_index]

    # Find the index of the selected structure in the original graphene list
    p6_index = graphene.index(selected_structure)
    # Return the single atoms object with the selected structure
    graphene = graphene[p6_index]

    return graphene


def cleave_amorphous(graphene, vacuum):
    """
    Summary
    ----------
    Add rotated functional group to ribbon

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    vacuum : float
        Vacuum to be added to cell
    """

    graphene_cp = graphene.copy()

    # First create vacuum in x direction and then position sheet in the centre
    positions = graphene_cp.get_positions()
    cell = graphene_cp.get_cell()

    cell[0, 0] += 2 * vacuum
    positions[:, 0] += vacuum

    graphene_cp.set_cell(cell)
    graphene_cp.set_positions(positions)

    # Compute neighbor list after cleaving
    n1, n2 = neighborlist.neighbor_list(
        "i" "j", graphene_cp, cutoff=1.85, self_interaction=False
    )

    # Then we delete any dangling atom on the surface which has only one neighbour
    coord = np.bincount(n1)
    delete = []
    while 1 in coord:
        for i in range(len(coord)):
            if coord[i] == 1:
                delete.append(i)
                coord[i] = 0
                # We need to check if removing the atom creates more dangling atoms, so we look at the coordination of its neigbors
                neighbors = n2[n1 == i]
                for n in neighbors:
                    coord[n] -= 1

    graphene_cp = graphene_cp[[i for i in range(len(graphene_cp)) if i not in delete]]

    return graphene_cp


def saturate_amorphous(graphene, nn_list, box_size, CH_bond=1.09):
    """
    Summary
    ----------
    Add rotated functional group to ribbon

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    nn_list : numpy.ndarray
        Array of nearest neighbours
    vacuum : float
        Vacuum to be added to cell
    """
    coord = np.bincount(nn_list[:, 0].T)
    for i in range(len(coord)):
        if coord[i] == 2:
            neighbors = nn_list[:, 1][nn_list[:, 0] == i]
            bond_vector_1 = graphene[neighbors[0]].position - graphene[i].position
            bond_vector_1 = utilities.minimum_image(bond_vector_1, box_size)
            bond_vector_2 = graphene[neighbors[1]].position - graphene[i].position
            bond_vector_2 = utilities.minimum_image(bond_vector_2, box_size)
            scale_factor = CH_bond / np.linalg.norm(bond_vector_1 + bond_vector_2)
            bond_vector_ch = -1 * scale_factor * (bond_vector_1 + bond_vector_2)
            H_pos = graphene[i].position + bond_vector_ch
            graphene.append(Atom("H", H_pos))

    return graphene
