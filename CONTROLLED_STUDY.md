# Controlled Baby U-Net study

**Question.** Which bottleneck interventions reliably change a specific segmentation error?

## Split and training

Freeze a split manifest before running the study. Include stable examination IDs, patient IDs where available, and split assignments. Group all images from a patient together. Verify whether the Montgomery filename identifier is a valid patient grouping key before treating the historical filename split as patient-level separation. Record any identity limitations in the report. The course test set has already been used for reporting and figures. For a confirmatory claim, reserve an untouched cohort, or label an analysis on existing data as retrospective.

Use the same fixed split, preprocessing, and checkpoint selection rule for five independently initialized Baby U-Nets. Keep the training seed separate from the split seed. Select checkpoints using validation Dice. Freeze the probability threshold at 0.5. Record exact dependency versions, code revision, split fingerprint, and checkpoint hash for every run.

## Select channels and intervene

1. Choose one primary error before inspecting test predictions. A concrete starting hypothesis is that zeroing some channels reduces false positives near the lung boundary. Specify the boundary band in pixels at the fixed input resolution, the denominator for the error rate, and an acceptable increase in false negatives before running.
2. For each seed, rank single-channel interventions on validation by reduction in the primary error, subject to the false-negative limit. Freeze the selected channel or group, selection rule, and any group size before test evaluation. Use sparsity, overlays, and correlation clusters for describing or proposing candidates on validation. Channel indices are checkpoint-local.
3. Compare intact inference, zeroing the selected channels, and zeroing randomly sampled sets of the same size from the same bottleneck. Draw controls without replacement within each set and record the sampling seed. Report an activity-matched sensitivity analysis using validation activations to check whether the comparison is driven by inactive controls. Enumerate eligible controls for single-channel tests when feasible.
4. Evaluate each intervention on the same held-out examples. Save per-image Dice, IoU, false-positive and false-negative rates, and the primary boundary error with its denominator. Aggregate over images with equal weights, report paired effects and patient-level bootstrap intervals, and show the target's position in the control distribution separately for each training seed. Record representative improvements, regressions, and unchanged masks using prespecified selection rules.

Evidence for the hypothesis would be a repeatable reduction in the primary error relative to matched controls, with the false-negative tradeoff within the prespecified limit. Stable effects across seeds support the intervention rule. Identifying a shared anatomical feature would require a separate cross-seed alignment analysis and independent anatomical evidence.

## Release preparation

Keep the shared course artifact and its archival outputs as the basis for team review. Develop the study runner, manifests, and new results on a separate fork branch. Before a public release, agree on authorship and licensing, verify redistribution terms for data-derived images and checkpoints, record exact reproduction commands and environment versions, and tag a reviewable revision. Store data and weights separately as appropriate. The first implementation milestone is a per-image evaluator that uses the existing hook-based zeroing, records paired metrics, and verifies a zero-channel intervention reproduces intact predictions.
