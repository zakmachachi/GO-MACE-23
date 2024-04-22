"""_summary_
This script generates a decorated graphene oxide structure from pristine graphene. 

#TODO: Define how we are going to run over p3 (structural disorder) and p4 (edge functionalisation) parameters
#TODO: Do we want to use load atoms? Or should we ship the disorderd structures with the code?

"""

import time

import amorphous
import bulk_oxidation
import edge_oxidation
import numpy as np
from ase import neighborlist
from ase.io import write


class build:
    """_summary_
    This class contains all the functions required to build the graphene oxide structure
    """

    def __init__(self):
        pass

    def main(
        self,
        graphene,
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

        if disorder:
            graphene = amorphous.select_disordered(p6, graphene)

        if 8 in graphene.numbers:
            # delete the O atoms
            graphene = graphene[graphene.numbers != 8]
            # delete the H atoms
            if 1 in graphene.numbers:
                graphene = graphene[graphene.numbers != 1]

        # Get the box size
        box_size = graphene.get_cell().diagonal()

        if disorder and edges:
            graphene = amorphous.cleave_amorphous(graphene, vacuum)

        # Build NeighborList object
        i, j = neighborlist.neighbor_list(
            "i" "j", graphene, cutoff=1.85, self_interaction=False
        )
        nn_list = np.array((i, j)).T

        if disorder and edges:
            graphene = amorphous.saturate_amorphous(graphene, nn_list, box_size)

        # Run edge functionalisation if requested by user
        if edges:
            # Get indices of H atoms from graphene sheet
            h_atoms = np.array(np.where(graphene.get_atomic_numbers() == 1))[0][:]
            # Store number of H atoms
            N_hydrogen = h_atoms.shape[0]
            # First we need to add the edge carbons to the oxidized carbon list, so we do not oxidise them again in the 2D code
            edge_atoms = edge_oxidation.get_edge_carbons(graphene)
            # Create neighbor list which contains the collision zone of each H atom
            H = graphene[graphene.numbers == 1]
            neighbors = (
                np.array(neighborlist.neighbor_list("ij", H, 2.55)).T + h_atoms[0]
            )
            # Create a list to keep track of functionalised H atoms
            funct_atoms = np.array([])
            # Calculate number of each fuctional group to be added
            N_groups = int(p4 * N_hydrogen)
            # Add edge functionality to graphene
            graphene, edge_atoms, N_edge_added = edge_oxidation.add_edge_functionality(
                graphene,
                edge_atoms,
                h_atoms,
                funct_groups,
                1.4,
                N_groups,
                funct_atoms,
                neighbors,
                box_size[0],
                max_iterations,
            )
            # We also need to calculate the number of bulk atoms so we know how many atoms we can oxidise later
            bulk = graphene[[i for i in range(len(graphene)) if i not in edge_atoms]]
            N_atoms = len(bulk)
        else:
            # If no edges present we have no edge atoms and all atoms can be oxidised
            edge_atoms = []
            N_atoms = len(graphene)

        # Edge atoms are added to oxidised carbon list to avoid oxidising them
        oxidised_atoms = edge_atoms

        # Oxygen content of the graphene oxide is dependant on the OH ratio
        # This is because the epoxy group will oxidise 2 carbon atoms whereas the hydroxyl group will oxidise 1 carbon atom
        # The number of oxygen atoms is calculated as follows:

        n_O = round(O_content * N_atoms)  # Number of O atoms
        n_OH = round(OH_ratio * n_O)  # Number of hydroxyl groups
        n_epoxy = n_O - n_OH  # Number of epoxy groups

        # Buckling for the oxygen atoms (in Angstroms)
        buckling_epoxy = np.arange(0.1, 0.16, 0.01)
        buckling_OH = np.arange(0.1, 0.36, 0.01)

        # We will add the the oxygen atoms in two different ways:
        # 1. Add the oxygen atoms above the carbon atoms at the midpoint of the bond (epoxy groups).
        # 2. Add the oxygen atoms above a carbon atom (hydroxyl groups)

        (
            graphene,
            oxidised_atoms,
            n_epoxy_added,
            close_positions_up,
            close_positions_down,
        ) = bulk_oxidation.add_epoxy_group(
            graphene,
            oxidised_atoms,
            n_epoxy,
            buckling_epoxy,
            n_O,
            n_OH,
            N_atoms,
            nn_list,
            box_size,
            max_iterations,
        )
        graphene, oxidised_atoms, n_OH_added = bulk_oxidation.add_hydroxyl_group(
            graphene,
            oxidised_atoms,
            n_OH,
            buckling_OH,
            N_atoms,
            nn_list,
            close_positions_up,
            close_positions_down,
            max_iterations,
        )

        graphene.rattle(0.02)

        # Write the functionalised graphene oxide structure to a file
        write(
            output_structure,
            graphene,
        )

        print(
            "Successfully functionalised graphene to generate graphene oxide structure"
        )
        print(f"Added {n_epoxy_added} epoxy groups out of {n_epoxy} requested")
        print(f"Added {n_OH_added} hydroxyl groups out of {n_OH} requested")
        if edges:
            print(f"Added {N_edge_added} edge groups out of {N_groups} requested")
        print("Time taken: {:.2f} seconds".format(time.time() - start_time))

        pass
