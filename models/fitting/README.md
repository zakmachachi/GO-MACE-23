## Information regarding the iterations and DFT settings used for our MACE fit
0) **iter-0:** Seeded in CASTEP-GAP (5x5 matrix) - all relevant structures were taken from the CASTEP-GAP runs up over 10 ps. A filter of any bond length < 0.5 and coordination > 6 was applied to remove high E/F structures.

1) **iter-1:** iter-0 + structures held at 600K using MACE model fitted on iter-0. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

2) **iter-2:** iter-1 + structures held at 900K using MACE model fitted on iter-1. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

3) **iter-3:** iter-2 + structures held at 1200K using MACE model fitted on iter-2. This potential was unstable and led to failed runs at 0.40-0.00 and 0.50-0.25. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

4) **iter-4:** iter-3 + structures held at 1500K using MACE model fitted on iter-3. This potential was unstable and led to failed runs at 0.50-0.00 and 0.50-0.25. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

5) **iter-5:** iter-4 + structures held at 1500K using MACE model fitted on iter-4.  This potential was unstable and led to failed runs at 0.40-0.00 and 0.50-0.75. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

6) **iter-6:** iter-5 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

7) **iter-7:** iter-6 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

8) **iter-8:** iter-7 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

9) **iter-9:** iter-8 + edge structures held at 1500K using MACE model fitted on iter-8. Initial structures were sampled across p1 and p3 from 0.1-0.5 (p2 = 0.5). 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

10) **iter-10:** iter-9 + edge structures held at 1500K using MACE model fitted on iter-9. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

11) **iter-11:** iter-10 + edge structures held at 1500K using MACE model fitted on iter-10. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

12) **iter-12:** iter-11 + edge structures held at 1500K using MACE model fitted on iter-11. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed. iter-12 was cleaned up by removing any structures with forces > 50 eV/A. 7 Structures were removed from the training data and 0 from the test data.

The production model can be found in iter-12-final-model. The final database can be found in iter-12-clean/structures/iter-12-train-filtered.xyz.

## MACE fitting settings:

    --name="MACE_model" \
    --train_file="" \
    --valid_fraction=0.10 \
    --test_file="" \
    --config_type_weights='{"Default":1.0}' \
    --E0s='{1:-13.59395639138, 6:-148.314002, 8:-432.8647463978}' \
    --model="MACE" \
    --hidden_irreps='128x0e' \
    --loss='huber' \
    --r_max=3.7 \
    --batch_size=25 \
    --max_num_epochs=1200 \
    --swa \
    --default_dtype='float32' \
    --energy_key='QM_energy' \
    --forces_key='QM_forces' \
    --stress_key=None \
    --start_swa=500 \
    --ema \
    --ema_decay=0.99 \
    --amsgrad \
    --restart_latest \
    --device=cuda \
    --seed=123 \

## DFT settings (CASTEP 23.1):

    calculate_stress = false
    popn_calculate = false
    xc_functional   PBE 
    spin_polarized : false
    mixing_scheme : Pulay
    cut_off_energy = 550 eV
    elec_energy_tol = 1e-5 eV
    max_scf_cycles  200
    fix_occupancy   false
    opt_strategy    speed
    smearing_scheme Gaussian
    smearing_width 0.1 eV
    WRITE_CHECKPOINT : MINIMAL
    
