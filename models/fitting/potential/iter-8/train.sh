#!/bin/bash

gpu_id=0
CUDA_VISIBLE_DEVICES="$gpu_id" python /u/vld/sedm6197/software/mace/scripts/run_train.py \
    --name="MACE_model" \
    --train_file="structures/iter-8-train.xyz" \
    --valid_fraction=0.10 \
    --test_file="structures/iter-8-test.xyz" \
    --config_type_weights='{"Default":1.0}' \
    --model="ScaleShiftMACE" \
    --hidden_irreps='128x0e+128x1o' \
    --loss='huber' \
    --r_max=3.7 \
    --batch_size=30 \
    --max_num_epochs=2000 \
    --swa \
    --default_dtype='float32' \
    --energy_key='QM_energy' \
    --forces_key='QM_forces' \
    --stress_weight=0 \
    --stress_key=None \
    --start_swa=1000 \
    --swa_energy_weight=1000 \
    --swa_forces_weight=100 \
    --lr=0.001 \
    --ema \
    --ema_decay=0.99 \
    --amsgrad \
    --restart_latest \
    --device=cuda \
    --seed=123 \
