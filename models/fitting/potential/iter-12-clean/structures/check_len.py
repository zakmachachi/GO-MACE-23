from ase.io import read

atoms = read('iter-12-train-filtered.xyz', index=':')
num_atoms = []
for structure in atoms:
    num_atoms.append(len(structure))
print(sum(num_atoms))