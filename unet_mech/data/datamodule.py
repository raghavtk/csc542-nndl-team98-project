from __future__ import annotations

from typing import Tuple

import torch
from loguru import logger
from torch.utils.data import DataLoader, Subset, random_split
from torchvision import transforms
from torchvision.transforms import InterpolationMode
from torchvision.transforms import functional as TF

from unet_mech.config import IMAGENET_MEAN, IMAGENET_STD
from unet_mech.data.dataset import MontgomeryDataset


class PairedTrainTransform:
    """Apply geometric augmentation identically to an image/mask pair."""

    def __init__(
        self,
        hflip_p: float = 0.5,
        rotation_degrees: float = 8.0,
        brightness: float = 0.15,
        contrast: float = 0.15,
    ):
        self.hflip_p = hflip_p
        self.rotation_degrees = rotation_degrees
        self.color_jitter = transforms.ColorJitter(
            brightness=brightness,
            contrast=contrast,
        )

    def __call__(self, image: Image.Image, mask: Image.Image):
        if torch.rand(()) < self.hflip_p:
            image = TF.hflip(image)
            mask = TF.hflip(mask)

        angle = (
            torch.empty(1)
            .uniform_(-self.rotation_degrees, self.rotation_degrees)
            .item()
        )
        image = TF.rotate(image, angle, interpolation=InterpolationMode.BILINEAR)
        mask = TF.rotate(mask, angle, interpolation=InterpolationMode.NEAREST)
        image = self.color_jitter(image)
        return image, mask


def make_transforms(
    img_size: int,
    image_mode: str = "RGB",
) -> Tuple[transforms.Compose, transforms.Compose, transforms.Compose, transforms.Compose]:
    """Returns (train_img_tf, train_mask_tf, val_img_tf, val_mask_tf)."""
    mean, std = {
        "RGB": (IMAGENET_MEAN, IMAGENET_STD),
        "L": ([0.5], [0.5]),
    }[image_mode]
    train_img_tf = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ]
    )

    train_mask_tf = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )

    val_img_tf = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ]
    )

    val_mask_tf = transforms.Compose(
        [
            transforms.ToTensor(),
        ]
    )

    return train_img_tf, train_mask_tf, val_img_tf, val_mask_tf


def build_dataloaders(
    root: str,
    batch_size: int,
    img_size: int,
    train_frac: float,
    val_frac: float,
    seed: int,
    num_workers: int = 2,
    image_mode: str = "RGB",
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Split dataset into train / val / test DataLoaders.
    Val and test splits use inference-only transforms.
    """
    train_img_tf, train_mask_tf, val_img_tf, val_mask_tf = make_transforms(img_size, image_mode)

    full_ds = MontgomeryDataset(
        root=root,
        img_size=img_size,
        transform=train_img_tf,
        mask_transform=train_mask_tf,
        joint_transform=PairedTrainTransform(),
        image_mode=image_mode,
    )

    n = len(full_ds)
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    n_test = n - n_train - n_val

    gen = torch.Generator().manual_seed(seed)
    train_ds, val_ds, test_ds = random_split(
        full_ds, [n_train, n_val, n_test], generator=gen
    )

    eval_ds = MontgomeryDataset(
        root=root,
        img_size=img_size,
        transform=val_img_tf,
        mask_transform=val_mask_tf,
        image_mode=image_mode,
    )
    val_ds = Subset(eval_ds, val_ds.indices)
    test_ds = Subset(eval_ds, test_ds.indices)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    logger.info(
        f"[data] Split → train: {len(train_ds)}, val: {len(val_ds)}, test: {len(test_ds)}"
    )
    return train_loader, val_loader, test_loader
