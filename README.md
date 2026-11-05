# Unpacking the U-Net Bottleneck

Course artifact for CSC 542 Neural Networks and Deep Learning, Spring 2026. Team 98 members are Pranav Bhagwat, Raghav Kesari, and Tiehang Zhang.

## What the team built

- **Pranav Bhagwat, architecture and data.** [Scratch Baby U-Net notebook](baby_Unet.ipynb), [original pretrained ResNet-18 baseline notebook](notebooks/resnet18_baseline_course.ipynb), and [initial proposal](project_proposal.md).
- **Raghav Kesari, feature visualization.** [Toy CNN prototype](Interpretability_ToyCNN.ipynb), [channel grids and overlays](outputs/bottleneck_viz), and [sparsity and lung selectivity scores](outputs/sparsity_scores.csv). The [original handoff](HANDOFF.md) records the team's working interpretations.
- **Tiehang Zhang, ablation and failure analysis.** [Single-channel ablation](outputs/baby_unet_analysis_full/bottleneck_ablation_val.csv), [test predictions](outputs/baby_unet_analysis_full/test_predictions.png), and [correlation and group ablation report](correlation_analysis_report.md).

The integration branch contains the original Git histories. Course main is `9711f8e`, `dev` is `32bc73d`, `ablation` is `c03fd41`, and `person2-sparsity` is `2c342bf`. The `ablation` branch already contains `dev`. Both divergent tips are parents of the integration merge. The top-level baseline notebook is the later modular version.

## Reproduce locally

Run from this directory with Python 3.10 or later. Create a virtual environment and install `requirements.txt`. PyTorch and torchvision must be a compatible pair. On Windows, the commands below can use `./.venv/Scripts/python.exe` after creating the environment with `python -m venv .venv`.

For this local copy, the checkpoint and the 138 image/mask pairs were extracted from the course ZIP. The checkpoint is `baby_unet_best.pth` with SHA-256 `b6d681f7ac139e81ddb837d1864c0109f5e967335ea04c716bde30b7607cb5ca`. The dataset goes under `data/montgomery/MontgomerySet`. The loader can obtain Montgomery data if that directory is missing. For scratch training and checkpoint creation, use `baby_Unet.ipynb`. For the separate pretrained baseline, use `scripts/train_baseline.py`.

```bash
python -m pip install -r requirements.txt
python scripts/run_ablation.py --ckpt baby_unet_best.pth --split test --channels "" --out-csv outputs/rerun/test_baseline.csv
python scripts/run_ablation.py --ckpt baby_unet_best.pth --from-ch 0 --to-ch 128
python scripts/run_bottleneck_viz.py --ckpt baby_unet_best.pth --num-samples 3 --overlay-ch 118
python scripts/run_sparsity.py --ckpt baby_unet_best.pth
python scripts/run_channel_correlation.py --ckpt baby_unet_best.pth --ablation-csv outputs/rerun/ablation_sweep.csv
```

The baseline-only command prints IoU and Dice to the console and writes a header-only ablation CSV. The exploratory commands default to validation and save new outputs under `outputs/rerun/`. Baby U-Net takes one grayscale channel normalized to [-1, 1]. The pretrained baseline takes ImageNet-normalized RGB. Both return probabilities and use a threshold of 0.5. Baby U-Net exposes `bottleneck`, also available as the original `enc_layer4` hook name.

## How to read the archived results

The [full historical metrics CSV](outputs/baby_unet_analysis_full/baseline_metrics.csv) records test Dice **0.9353** and IoU **0.8795** on 22 images. The smaller `baby_unet_analysis` run and the Person 2 sweep are separate historical outputs. The checked-in figures and numbers are archived course results. Runtime reproduction still requires the Python dependencies.

Gini summarizes spatial concentration, and lung selectivity compares activation inside and outside the mask. Anatomical labels in the handoff are hypotheses. The reported group and single-channel interventions measure changes under zeroing in the studied model. They provide exploratory evidence about channel contributions and leave anatomical specificity, redundancy, and stability across training seeds open.

The [controlled study protocol](CONTROLLED_STUDY.md) defines the follow-on experiment and the evidence needed before preparing a public release.
