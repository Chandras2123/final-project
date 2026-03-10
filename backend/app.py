from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import shutil
import os
import nibabel as nib
import cv2
import numpy as np
import traceback

from classifier import classify_slices, classify_image
from pipeline.preprocess import load_and_preprocess
from pipeline.inference import load_model, predict_volume
from pipeline.postprocess import clean_mask
from pipeline.mesh import brain_mask, save_mesh

# ==========================================

# APP INIT

# ==========================================

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# ==========================================

# LOAD SEGMENTATION MODEL

# ==========================================

MODEL_PATH = "teacher_3d_unet.h5"
SEG_MODEL = load_model(MODEL_PATH)

print("✅ Segmentation model loaded")

# ==========================================

# MRI IMAGE VALIDATION

# ==========================================

def is_brain_mri_image(img):
 try:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = gray.shape
    if h < 80 or w < 80:
        return False

    b, g, r = cv2.split(img)
    color_diff = np.mean(abs(b-g)) + np.mean(abs(g-r))

    if color_diff > 60:
        return False

    std = np.std(gray)
    if std < 10:
        return False

    return True

 except:
    return False

# ==========================================

# NIFTI VALIDATION

# ==========================================

def is_valid_nifti(path):
 try:
    nii = nib.load(path)
    data = nii.get_fdata()

    if data.ndim < 3:
        return False

    return True

 except:
    return False

# ==========================================

# UPLOAD API

# ==========================================

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
 try:

    filename = file.filename.lower()
    input_path = os.path.join("uploads", filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("📂 Received file:", filename)

    # IMAGE MODE
    if filename.endswith((".jpg", ".jpeg", ".png")):

        img = cv2.imread(input_path)

        if img is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid image file."
            )

        if not is_brain_mri_image(img):
            raise HTTPException(
                status_code=400,
                detail="Please upload a Brain MRI image."
            )

        tumor_type = classify_image(img)

        return {
            "mode": "image_classification",
            "tumor_type": tumor_type
        }

    # NIFTI MODE
    elif filename.endswith((".nii", ".nii.gz")):

        if not is_valid_nifti(input_path):
            raise HTTPException(
                status_code=400,
                detail="Invalid NIfTI MRI file."
            )

        volume, affine = load_and_preprocess(input_path)

        tumor_type = classify_slices(volume)

        prob_map = predict_volume(volume, SEG_MODEL)

        tumor_mask = clean_mask(prob_map)

        tumor_nii = nib.Nifti1Image(tumor_mask.astype("uint8"), affine)

        mask_path = "outputs/tumor_mask.nii.gz"
        nib.save(tumor_nii, mask_path)

        brain = brain_mask(volume)

        brain_mesh_path = "outputs/brain_mesh.obj"
        tumor_mesh_path = "outputs/tumor_mesh.obj"

        save_mesh(brain, brain_mesh_path)
        save_mesh(tumor_mask, tumor_mesh_path)

        return {
            "mode": "3d_analysis",
            "tumor_type": tumor_type,
            "mask": mask_path,
            "brain_mesh": brain_mesh_path,
            "tumor_mesh": tumor_mesh_path,
            "file_path": input_path
        }

    else:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

 except HTTPException as e:
    raise e

 except Exception:

    print("❌ ERROR")
    traceback.print_exc()

    raise HTTPException(
        status_code=500,
        detail="Internal server error"
    )

# ==========================================

# MRI SLICE VIEWER API

# ==========================================

@app.get("/slices")
def get_mri_slices(path: str = Query(...)):
 img = nib.load(path)
 data = img.get_fdata()

 slices = []

  for i in range(data.shape[2]):

    slice_img = data[:, :, i]

    slice_img = (slice_img - slice_img.min()) / (slice_img.max() - slice_img.min() + 1e-8)

    slices.append(slice_img.tolist())

 return {"slices": slices}
