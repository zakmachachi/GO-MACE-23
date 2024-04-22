## Some info regarding the iterations and DFT settings used for our MACE fit
## Potential-3
0) iter-0: Seeded in CASTEP-GAP (5x5 matrix) - all relevant structures were taken from the CASTEP-GAP runs up over 10 ps. A filter of any bond length < 0.5 and coordination > 6 was applied to remove high E/F structures.

1) iter-1: iter-0 + structures held at 600K using MACE model fitted on iter-0. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

2) iter-2: iter-1 + structures held at 900K using MACE model fitted on iter-1. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

3) iter-3: iter-2 + structures held at 1200K using MACE model fitted on iter-2. This potential was unstable and led to failed runs at 0.40-0.00 and 0.50-0.25. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

4) iter-4: iter-3 + structures held at 1500K using MACE model fitted on iter-3. This potential was unstable and led to failed runs at 0.50-0.00 and 0.50-0.25. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

5) iter-5: iter-4 + structures held at 1500K using MACE model fitted on iter-4.  This potential was unstable and led to failed runs at 0.40-0.00 and 0.50-0.75. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

6) iter-6: iter-5 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

7) iter-7: iter-6 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

8) iter-8: iter-7 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

9) iter-9: iter-8 + edge structures held at 1500K using MACE model fitted on iter-8. Initial structures were sampled across p1 and p3 from 0.1-0.5 (p2 = 0.5). 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

10) iter-10: iter-9 + edge structures held at 1500K using MACE model fitted on iter-9. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

11) iter-11: iter-10 + edge structures held at 1500K using MACE model fitted on iter-10. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

12) iter-12: iter-11 + edge structures held at 1500K using MACE model fitted on iter-11. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed. iter-12 was cleaned up by removing any structures with forces > 50 eV/A. 7 Structures were removed from the training data and 0 from the test data

## Negative control
0) iter-0: Fitted on 820 AIMD structures held at 300K for 10 ps for two ratios, 0.10-0.50 and 0.50-0.50. 

1) iter-1: iter-0 + structures held at 600K using MACE model fitted on iter-0. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

2) iter-2: iter-1 + structures held at 900K using MACE model fitted on iter-1. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

3) iter-3: iter-2 + structures held at 1200K using MACE model fitted on iter-1. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

4) iter-4: iter-3 + structures held at 1500K using MACE model fitted on iter-3. This potential was unstable and led to failed runs at 0.20-0.25, 0.30-0.00, 0.30-0.25, 0.30-0.50, 0.50-0.00, 0.50-0.25, 0.50-0.50. As a result, all structures from every trajectory were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures.

5) iter-5: iter-4 + structures held at 1500K using MACE model fitted on iter-3. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

6) iter-6: iter-5 + structures held at 1500K using MACE model fitted on iter-3. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

7) iter-7: iter-6 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

8) iter-8: iter-7 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

9) iter-9: iter-8 + edge structures held at 1500K using MACE model fitted on iter-8. Initial structures were sampled across p1 and p3 from 0.1-0.5 (p2 = 0.5). 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed. All H atoms flew off at the start. 

10) iter-10: iter-9 + edge structures held at 1500K using MACE model fitted on iter-9. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

11) iter-11: iter-10 + edge structures held at 1500K using MACE model fitted on iter-10. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

12) iter-12: iter-11 + edge structures held at 1500K using MACE model fitted on iter-11. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed. iter-12 was cleaned up by removing any structures with forces > 50 eV/A. 9 Structures were removed from the training data and 8 from the test data

## Potential-2
0) iter-0: Seeded in CASTEP-GAP (5x5 matrix) - all relevant structures were taken from the CASTEP-GAP runs up over 10 ps. A filter of any bond length < 0.5 and coordination > 5 was applied to remove high E/F structures

2) iter-1: iter-0 + structures held at 600K using MACE model fitted on iter-0. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed

3) iter-2: iter-1 + structures held at 900K using MACE model fitted on iter-1. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed

4) iter-3: iter-2 + structures held at 1200K using MACE model fitted on iter-2. This potential was much more unstable and led to failed runs. As a result, all structures were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures. 

5) iter-4: iter-3 + structures held at 1500K using MACE model fitted on iter-3. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed

6) iter-5: iter-4 + structures held at 1500K using MACE model fitted on iter-4. This potential was unstable and led to failed runs. As a result, all structures were taken and were filtered according to: min bond length < 0.5 were discarded, isolated atoms were deleted, no atoms with > 6 coordination. The structures were then downsampled using FPS to 250 structures. 

7) iter-6: iter-5 + structures held at 1500K using MACE model fitted on iter-5. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

8) iter-7: iter-6 + structures held at 1500K using MACE model fitted on iter-6. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

9) iter-8: iter-7 + structures held at 1500K using MACE model fitted on iter-7. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix). Structures were cleaned where single atoms were removed.

10) iter-9: iter-8 + edge structures held at 1500K using MACE model fitted on iter-8. Initial structures were sampled across p1 and p3 from 0.1-0.5 (p2 = 0.5). 

## Potential-1
1) iter-0: Seeded in CASTEP-GAP (5x5 matrix) - structures were filtered as some runs failed. Any bond length < 0 was discarded. This lead to 769 training configs and 50 validation. Subsequent MACE model was fitted (settings below).

2) iter-1: iter-0 + structures held at 600K using MACE model fitted on iter-0. 250 structures were added (1 ps intervals (10 ps total) on 5x5 matrix)

3) iter-2: iter-1 + structures held at 900K. 250 structures added

4) iter-3: iter-2 + structures held at 1200K. 250 structures added

5) iter-4: iter-3 + structures which were continiously failing at 1500K. Ramps did not help. Structures which were chosen are:

composition = ['0.30-0.00', '0.40-0.00', '0.40-0.50', '0.50-0.00', '0.50-0.25']*5

5 of each composition was run and some would continiously fail. Regardless, we sampled every 0.2 ps and discarded any structures which had failed using the same filtering technique. This gave us 275 structures 

{'0.30-0.00': 50 , '0.40-0.00': 52 , '0.40-0.50': 135, '0.50-0.00': 26, '0.50-0.25': 12}

6) iter-5: iter-4 + repeated the same compositions. This time we had 1015 structures after filtering -> the potential is getting more stable. We used farthest point sampling to reduce the sampling space down to 275 structures. iter-5 would fail in the regime of forming esther groups, 5 membered rings and also 3 coordinate O atoms inside of 6 membered rings. See 1500K-epox-3 0.3-0.00-x etc..

7) iter-6: same as iter-5

8) iter-7: same as iter-6. The potential is still unstable. 

9) iter-8: Repeated the high epoxide runs, but now we use a more lenient filtering system (0.5 A and >5 coordinate). We also pushed in all of the data rather than using FPS. We have 922 structures. It is now stable

10) iter-9: Begin iterations over p3 space (degree of structural disorder)

MACE fitting settings:

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

DFT settings (CASTEP 23.1):

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
    