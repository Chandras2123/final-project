import numpy as np
from scipy.ndimage import label, binary_fill_holes

def clean_mask(prob, threshold=0.5):
    mask = (prob > threshold).astype(np.uint8)

    labeled, n = label(mask)
    if n > 1:
        sizes = [(labeled == i).sum() for i in range(1, n + 1)]
        mask = (labeled == (sizes.index(max(sizes)) + 1))

    mask = binary_fill_holes(mask)
    return mask.astype(np.uint8)
