import nibabel as nib
import numpy as np

def load_and_preprocess(nii_path):
    nii = nib.load(nii_path)
    vol = nii.get_fdata()  # (H, W, D, C)

    # ✔ Select FLAIR channel
    if vol.ndim == 4:
        vol = vol[..., 3]

    # Normalize (z-score)
    mean, std = vol.mean(), vol.std()
    vol = (vol - mean) / (std + 1e-8)

    return vol.astype(np.float32), nii.affine
