# How we assembled the Team 98 course project

Team 98 built a model that marks the lungs in chest X-rays and explored which parts of the model influence those markings. This document records how the three teammates' work was brought together, what the saved results show, and what a stronger follow-up experiment would require.

## Where the work lives

Git is the tool that records changes to the project. A **repository** is the project and its recorded history, a **fork** is a separate copy under another account, and a **clone** is a copy on your computer. A **commit** is a recorded version of the files. A **branch** is a named line of work, and a **merge** brings two lines of work together while keeping their histories.

The assembled project is in `mechinterp/csc542-nndl-team98-project`, the local clone of Raghav's GitHub fork. The assembly is on `course-artifact`. Its merge commit, `1ca5bb7`, brings together the two branches that continued independently after the initial class work.

- `main` at `9711f8e` holds the proposal and initial notebooks. A **notebook** combines runnable code, written explanation, and saved outputs in one file.
- `dev` at `32bc73d` reorganized the code into reusable pieces. Its history is already part of `ablation`.
- `ablation` at `c03fd41` adds the correlation report and code for testing groups of model features. An **ablation** is an experiment that disables a part of the model and measures how its output changes. **Correlation** measures how closely two signals vary together.
- `person2-sparsity` at `2c342bf` adds images that show where features respond and scores that describe those responses. **Sparsity** here means concentration of a feature's response in a small part of an image.

I kept the two branch histories because their recorded versions explain the differences between the original runs. The files in the merge are the starting point for reruns. The archived results remain evidence of what the team recorded at the time. This handoff is a separate commit so a team review can start at the assembly commit. [Project entry point](README.md)

## What each teammate contributed

**Pranav Bhagwat** handled data and model design. **Segmentation** means labeling each pixel, here as lung or background. A **mask** is the image of those labels. Baby U-Net is the team's compact segmentation model, trained from scratch. The team also used ResNet-18, an existing image model, as the first half of a separate segmentation model initialized with weights learned on another image collection. A **baseline** is a reference result or model used for comparison. I preserved the full original baseline notebook alongside the later, shorter version. [Baby U-Net notebook](baby_Unet.ipynb) · [Original baseline notebook](notebooks/resnet18_baseline_course.ipynb)

**Raghav Kesari** prototyped the feature displays on a smaller model and then applied them to Baby U-Net. The **bottleneck** is the middle of the model, where the image is represented on a smaller grid. Each **channel** is a separate map on that grid, and its **activations** are the numbers showing how strongly it responds at each location. An **overlay** places that response map over the source X-ray. The sparsity scores describe how concentrated a channel's response is, and the lung selectivity scores compare its average response inside and outside the lung mask. [Prototype notebook](Interpretability_ToyCNN.ipynb) · [Overlays](outputs/bottleneck_viz) · [Saved scores](outputs/sparsity_scores.csv)

**Tiehang Zhang** tested what happens when individual channels or groups are set to zero before the model finishes its prediction. The team recorded how the predicted masks changed and used correlation to identify channels with similar response patterns. [Single-channel results](outputs/baby_unet_analysis_full/bottleneck_ablation_val.csv) · [Group analysis](correlation_analysis_report.md)

## How the merged code fits together

A **checkpoint** is a saved set of learned model weights, the numbers the model adjusts during training. Those weights must be loaded into the corresponding model and used with the same **preprocessing**, the steps that convert a source image into the numbers the model expects.

The branches disagreed on two parts of that contract. I used the scratch-training notebook as the reference for Baby U-Net. It takes one grayscale image channel and rescales pixel values to the range −1 to 1. It produces a lung probability for each pixel. The ResNet-18 model uses three color channels and the scaling associated with its original training data. Both models mark a pixel as lung when its probability exceeds 0.5.

One shared loader now pairs each X-ray with its two lung outlines and selects the image preparation for the chosen model. A **split** assigns examples to training, validation, or test. Training fits the weights, validation guides choices, and the test split measures performance after those choices. The loader keeps the existing split rule and applies training-only image variations to the training set. It reads validation and test images without those variations. The model and image preparation are selected together in the commands that support both models.

The checkpoint and image files are local inputs recovered from the course ZIP. Git tracks the source, notebooks, and archived outputs. Reruns go into a separate results directory so the original evidence can still be reviewed. [Local run commands](README.md#reproduce-locally)

## What we can say today

**Dice** and **intersection over union (IoU)** measure how closely a predicted lung mask overlaps the reference mask. Both run from 0 for no overlap to 1 for perfect agreement. Dice divides twice the shared area by the sum of both mask areas. IoU divides the shared area by the total area covered by either mask. The full archived course run reports **0.9353 Dice** and **0.8795 IoU** on 22 test images. [Saved metrics](outputs/baby_unet_analysis_full/baseline_metrics.csv)

The displays and scores give the team candidates to investigate. A channel that responds near a lung edge could also respond to another structure. Zeroing a channel can show that it affects a prediction under that intervention. The course results leave open whether the effect is specific to a particular error and whether the effect repeats when the model is trained again.

I verified that all 138 X-rays have both lung-mask files, that the recovered checkpoint archive passes its integrity check and lists expected weight names, and that the Python files and notebook formats parse. The package installer could not obtain PyTorch, the software used to run the models. I therefore could not load the checkpoint into the merged model or independently reproduce the archived numbers.

## What the controlled study would add

A **controlled study** compares the intervention with a reference under the same conditions. Pick an error to measure before looking at test results, such as **false positives** near the lung edge, where the model marks background pixels as lung. Track **false negatives** as well, where the model misses pixels that belong to the lung.

Select candidate channels using validation images. On test images, compare the intact model, the model with the selected channels zeroed, and the model with an equal number of randomly selected channels zeroed. Repeat with several **training seeds**, numbers that set the starting state for randomized training steps. Keep images from the same patient together when patient identifiers can be established. The course test images have already been used in reporting, so reserve a fresh group of examples for an independent confirmation if one is available.

The proposed result is a consistent improvement on the chosen error compared with the random controls, with the cost in missed lung pixels measured alongside it. Before preparing an arXiv manuscript or public research package, the team can review the assembly, agree on how to credit and license the work, and verify which images and weights can be shared. [Proposed study protocol](CONTROLLED_STUDY.md)
