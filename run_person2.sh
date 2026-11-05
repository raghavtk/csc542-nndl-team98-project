#!/usr/bin/env bash
set -e
echo "Running ablation sweep..."
python scripts/run_ablation.py --ckpt baby_unet_best.pth --from-ch 0 --to-ch 128 --out-csv outputs/rerun/ablation_sweep.csv
echo "Running bottleneck visualization..."
python scripts/run_bottleneck_viz.py --ckpt baby_unet_best.pth --out-dir outputs/rerun/bottleneck_viz --max-ch 128 --num-samples 3
echo "Running sparsity scoring..."
python scripts/run_sparsity.py --ckpt baby_unet_best.pth --out-csv outputs/rerun/sparsity_scores.csv
echo "Done!"
