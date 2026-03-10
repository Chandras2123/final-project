import nibabel as nib
import numpy as np

def load_and_preprocess(path):

    img = nib.load(path)

    volume = img.get_fdata()

    affine = img.affine

    volume = volume.astype(np.float32)

    # normalize MRI
    volume = (volume - np.min(volume)) / (np.max(volume) - np.min(volume) + 1e-8)

    return volume, affine
