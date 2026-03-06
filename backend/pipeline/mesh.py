from skimage.measure import marching_cubes
import trimesh
import numpy as np
from scipy.ndimage import binary_fill_holes, label

def brain_mask(volume):
    mask = volume > np.percentile(volume, 20)
    mask = binary_fill_holes(mask)

    labeled, n = label(mask)
    if n > 1:
        sizes = [(labeled == i).sum() for i in range(1, n + 1)]
        mask = (labeled == (sizes.index(max(sizes)) + 1))

    return mask.astype(np.uint8)

def save_mesh(mask, out_path):
    verts, faces, _, _ = marching_cubes(mask, level=0.5)
    mesh = trimesh.Trimesh(verts, faces)
    mesh.export(out_path)
