import numpy as np
import utilities
from ase import Atom

user_asked = False


def add_epoxy_group(
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
):
    """_summary_
    Add an epoxy group to the graphene structure

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    oxidised_atoms: list
        List of the indices of the carbon atoms which have been oxidized
    n_epoxy : int
        Number of epoxy groups to add
    buckling_epoxy : list
        List of buckling heights for the epoxy groups
    n_O : int
        Number of oxygen atoms to add
    n_OH : int
        Number of hydroxyl groups to add
    N_atoms : int
        Number of atoms in the graphene structure
    nn_list : numpy.ndarray
        Array of nearest neighbours
    box_size : float
        Size of the box
    max_iterations : int
        Maximum number of iterations to try and add an epoxy group
    """
    # We are going to keep track of which carbons is the added oxygen close to(useful for collision checking)
    close_positions_up = []
    close_positions_down = []

    n_added = 0  # number of epoxy groups added
    while n_added < n_epoxy:
        # Choose a random carbon atom and its neighbour
        (
            graphene,
            oxidised_atoms,
            carbon_atom,
            neighbour,
            iterations,
        ) = pick_random_carbon(
            graphene,
            oxidised_atoms,
            N_atoms,
            nn_list,
            max_iterations,
            epoxy=True,
        )
        if carbon_atom is None and neighbour is None and iterations < max_iterations:
            pass
        elif carbon_atom is None and neighbour is None and iterations == max_iterations:
            print(
                f"Could not add {n_epoxy} epoxy groups as there are no more carbon atoms to oxidize."
            )
            break
        else:
            bond_vector = graphene[neighbour].position - graphene[carbon_atom].position
            bond_vector = utilities.minimum_image(bond_vector, box_size)
            midpoint = graphene[carbon_atom].position + bond_vector / 2

            # Add the oxygen atom (bond length of ~1.46 Angstroms, so ~1.26 Ang above the midpoint - https://arxiv.org/abs/1102.3797)
            # Calculate using basic trigonometry and we will place either above or below the midpoint

            rand = np.random.random()

            if rand < 0.5:
                graphene[carbon_atom].position += [
                    0,
                    np.random.choice(buckling_epoxy),
                    0,
                ]

                graphene[neighbour].position += [
                    0,
                    -1 * np.random.choice(buckling_epoxy),
                    0,
                ]

                graphene.append(Atom("O", midpoint + [0, 1.26, 0]))
                # We are going to say that the neighbours of the oxidised atoms to the close to the added epoxide, so that
                # if we oxidese any of them we know to check for a collisions between the OH and the epoxide
                # also we have seperate arrays for the top and the bottom oxygens
                for pair in nn_list:
                    if (
                        (pair[0] == carbon_atom or pair[0] == neighbour)
                        and pair[1] != carbon_atom
                        and pair[1] != neighbour
                    ):
                        close_positions_up.append([pair[1], len(graphene) - 1])

            elif rand >= 0.5:
                graphene[carbon_atom].position += [
                    0,
                    -1 * np.random.choice(buckling_epoxy),
                    0,
                ]

                graphene[neighbour].position += [0, np.random.choice(buckling_epoxy), 0]

                graphene.append(Atom("O", midpoint + [0, -1.26, 0]))

                for pair in nn_list:
                    if (
                        (pair[0] == carbon_atom or pair[0] == neighbour)
                        and pair[1] != carbon_atom
                        and pair[1] != neighbour
                    ):
                        close_positions_down.append([pair[1], len(graphene) - 1])
            # Add print statement saying we have added x % of the oxygen atoms
            n_added += 1
            print(f"Added {n_added} epoxy groups ({n_added/(n_O-n_OH)*100:.2f}%)")
    return graphene, oxidised_atoms, n_added, close_positions_up, close_positions_down


def add_hydroxyl_group(
    graphene,
    oxidised_atoms,
    n_OH,
    buckling_OH,
    N_atoms,
    nn_list,
    close_positions_up,
    close_positions_down,
    max_iterations,
):
    """_summary_
    Add a hydroxyl group to the graphene structure. Need to make sure we don't add a hydroxyl group to a carbon atom that already has an epoxy group.

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    oxidised_atoms : list
        List of the indices of the carbon atoms which have been oxidized
    n_OH : int
        Number of hydroxyl groups to add
    buckling_OH : list
        List of buckling heights for the hydroxyl groups
    N_atoms : int
        Number of atoms in the graphene structure
    nn_list : numpy.ndarray
        Array of nearest neighbours
    close_positions_up: np.ndarray
        Array of pairs of a carbon atom and nearby oxygen pointing up (used for collision checking)
        close_positions_down: np.ndarray
        Array of pairs of a carbon atom and nearby oxygen pointing down (used for collision checking)
    max_iterations : int
        Maximum number of iterations to try and add a hydroxyl group
    """
    n_added = 0
    # Add the oxygen atoms above a carbon atom (hydroxyl groups)
    while n_added < n_OH:
        # Choose a random carbon atom that doesn't already have an epoxy group
        (
            graphene,
            oxidised_atoms,
            carbon_atom,
            neighbour,
            iterations,
        ) = pick_random_carbon(
            graphene, oxidised_atoms, N_atoms, nn_list, max_iterations
        )

        if carbon_atom is None and iterations < max_iterations:
            pass
        elif carbon_atom is None and iterations == max_iterations:
            print(
                f"Could not add {n_OH-n_added} hydroxyl groups as there are no more carbon atoms to oxidize"
            )
            break

        else:
            # Hydroxyl groups added as first O and then H attached to it.
            # In both cases, it is critical to make sure that added atom is not in an unreasonably
            # close contact with other atoms. Below, check O atoms are positioned at least 1.85 Ang away
            # from other added O atoms. If not, delete appended O and search for another position.

            # Add the oxygen atom (bond lentgh of 1.49 Angstroms) either above or below the carbon atom

            rand = np.random.random()

            # buckling_OH = np.random.choice(buckling_OH)

            if rand < 0.5:
                graphene[carbon_atom].position += [0, np.random.choice(buckling_OH), 0]
                oxygen_pos = graphene[carbon_atom].position + [0, 1.49, 0]
                # get the collision zone of the added oxygen by looking at which oxygens are close to the oxidised C
                collision_zone = [
                    j[1] for j in close_positions_up if j[0] == carbon_atom
                ]

            elif rand >= 0.5:
                graphene[carbon_atom].position += [
                    0,
                    -1 * np.random.choice(buckling_OH),
                    0,
                ]
                oxygen_pos = graphene[carbon_atom].position + [0, -1.49, 0]
                collision_zone = [
                    j[1] for j in close_positions_down if j[0] == carbon_atom
                ]

            graphene.append(Atom("O", oxygen_pos))
            # If O of OH is close to other O atoms, delete OH and repeat search

            O_index = len(graphene) - 1

            # Check if structure is valid, i.e. if there are close contacts
            # Added oxygen atom is given as a an array (function originally was built for adding multi-atom groups)
            if utilities.is_structure_valid(graphene, [graphene[-1]], collision_zone):
                pass
            else:
                # If O is too close to other O atoms we delete it and undo the buckling
                del graphene[O_index]

                if rand < 0.5:
                    graphene[carbon_atom].position += [
                        0,
                        -1 * np.random.choice(buckling_OH),
                        0,
                    ]
                elif rand >= 0.5:
                    graphene[carbon_atom].position += [
                        0,
                        np.random.choice(buckling_OH),
                        0,
                    ]

                continue

            # Add the hydrogen atom (bond angle of 104.5 degrees and bond length of 0.98 Angstroms - https://arxiv.org/abs/1102.3797)
            # Calculate the hydrogen bond vector based on the orientation of the hydroxyl group

            bond_OH = 0.98

            theta_deg = 100.0 + np.random.random() * 15.0

            if rand < 0.5:
                theta = np.deg2rad(180 - theta_deg)
            elif rand >= 0.5:
                theta = np.deg2rad(theta_deg)

            phi = np.deg2rad(np.random.random() * 360.0)

            # Spherical to cartesian, add random orientation for OH

            x = bond_OH * np.sin(theta) * np.cos(phi)
            y = bond_OH * np.cos(theta)
            z = bond_OH * np.sin(theta) * np.sin(phi)

            H_pos = oxygen_pos + [x, y, z]
            graphene.append(Atom("H", H_pos))

            # Repeat the same collision zone analysis for the H atoms
            # If H of OH is close to other atoms, delete OH and repeat search
            H_index = len(graphene) - 1

            if utilities.is_structure_valid(graphene, [graphene[-1]], collision_zone):
                oxidised_atoms.append(carbon_atom)
                n_added += 1

                # Close C and O list is updated with new OH group
                # First we get the nearest neighbours of the oxidised carbon
                first_neighbors = nn_list[:, 1][nn_list[:, 0] == carbon_atom]
                # Then we want to collect the neighbours of the first neighbors as well
                second_neighbors = np.array([])
                for n in first_neighbors:
                    second_neighbors = np.concatenate(
                        [second_neighbors, nn_list[:, 1][nn_list[:, 0] == n]]
                    )
                    # close_positions_up.append([n, O_index])
                # We remove the duplicate second neighbours and also we removed the oxidised carbon
                second_neighbors = np.unique(second_neighbors)
                second_neighbors = second_neighbors[second_neighbors != carbon_atom]
                # now append selected C oxidized C list

                # collect first and second neighbors together
                # second_neighbors = second_neighbors.astype(int)
                neighbors = np.concatenate([first_neighbors, second_neighbors]).astype(
                    int
                )

                if rand < 0.5:
                    for n in neighbors:
                        close_positions_up.append([n, O_index])
                        close_positions_up.append([n, H_index])
                elif rand >= 0.5:
                    for n in neighbors:
                        close_positions_down.append([n, O_index])
                        close_positions_down.append([n, H_index])
            else:
                del graphene[H_index]
                del graphene[H_index - 1]

                if rand < 0.5:
                    graphene[carbon_atom].position += [
                        0,
                        -1 * np.random.choice(buckling_OH),
                        0,
                    ]

                elif rand >= 0.5:
                    graphene[carbon_atom].position += [
                        0,
                        np.random.choice(buckling_OH),
                        0,
                    ]

            print(f"Added {n_added} hydroxyl groups ({n_added/(n_OH)*100:.2f}%)")
            global user_asked
            if len(graphene) > 300 and user_asked == False:
                # stop the code and ask the user if they want to continue. if they do, then we will continue for the remainder of the entire code
                # if they don't then we will stop the code
                print(
                    "WARNING: Structure is getting large and will be out of range of DFT. Do you want to continue?"
                )
                user_input = input("Enter y to continue, anything else to stop: ")
                if user_input == "y":
                    user_asked = True  # Set the flag to True, so it won't ask again
                else:
                    print("Stopping code - Consider reducing the O content")
                    break
    return graphene, oxidised_atoms, n_added


def pick_random_carbon(
    graphene, oxidised_atoms, N_atoms, nn_list, max_iterations, epoxy=False
):
    """_summary_
    Pick a random carbon atom and its neighbour

    Parameters
    ----------
    graphene : ase.Atoms
        Graphene structure
    oxidised_atoms : list
        List of the indices of the carbon atoms which have been oxidized
    N_atoms : int
        Number of atoms in the graphene structure
    nn_list : numpy.ndarray
        Array of nearest neighbours
    epoxy : bool, optional
        If True, then we are adding an epoxy group, by default False
    """
    # Set the maximum number of iterations
    iterations = 0
    while iterations < max_iterations:
        # Create a list of all possible carbon atoms to choose from
        choices = list(range(N_atoms))
        # Remove the oxidised carbon atoms from the list of choices
        choices = [c for c in choices if c not in oxidised_atoms]
        # If choices is empty, then we have oxidised all the carbon atoms and we need to exit the function
        if epoxy:
            a = "epoxy"
        else:
            a = "hydroxyl"
        if len(choices) == []:
            print(f"All carbon atoms have been oxidised for {a}")
            return graphene, oxidised_atoms, None, None, iterations
        else:
            # Choose a random carbon atom
            carbon_atom = np.random.choice(choices)
            # Choose a random neighbour
            neighbours_store = nn_list[np.where(nn_list[:, 0] == carbon_atom)]
            # Remove the oxidised atoms from the list of neighbours
            neighbours = [n for n in neighbours_store[:, -1] if n not in oxidised_atoms]
            # If there are no neighbours, then we need to pick a new carbon atom
            if len(neighbours) == 0:
                print(
                    f"Iteration {iterations}: No neighbours found, picking new carbon atom"
                )
                iterations += 1
                # return graphene, oxidised_atoms, None, None
            else:
                neighbour = np.random.choice(neighbours)

                # Append oxidised carbon atom positions so we dont try and epoxy/hydroxyl group them again
                # oxidised_atoms.append(carbon_atom)

                if epoxy:
                    oxidised_atoms.append(carbon_atom)
                    oxidised_atoms.append(neighbour)  # append only oxidized atom

                # for OH, oxidised atoms are separately added to the list
                # after checking conditions of least distance for both O and H,
                # append C to oxidised atoms list.

                return (
                    graphene,
                    oxidised_atoms,
                    carbon_atom,
                    neighbour,
                    iterations,
                )
    print(
        f"WARNING: Maximum iterations reached for {a}. Check your structure to ensure it is correct"
    )
    return graphene, oxidised_atoms, None, None, iterations
