import numpy as np
import tensorflow as tf

PATCH = 128
STRIDE = 64

def dice_loss(y_true, y_pred):
    smooth = 1e-6
    inter = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    return 1 - (2 * inter + smooth) / (union + smooth)

def load_model(model_path):
    model = tf.keras.models.load_model(
        model_path,
        custom_objects={"dice_loss": dice_loss}
    )
    model.trainable = False
    return model

def predict_volume(volume, model,patch_size=128, stride=64):
    D, H, W = volume.shape
    prob = np.zeros((D, H, W), np.float32)
    count = np.zeros((D, H, W), np.float32)

    for x in range(0, D - PATCH + 1, STRIDE):
        for y in range(0, H - PATCH + 1, STRIDE):
            for z in range(0, W - PATCH + 1, STRIDE):
                patch = volume[x:x+PATCH, y:y+PATCH, z:z+PATCH]
                patch = patch[None, ..., None]

                pred = model.predict(patch, verbose=0)[0, ..., 0]

                prob[x:x+PATCH, y:y+PATCH, z:z+PATCH] += pred
                count[x:x+PATCH, y:y+PATCH, z:z+PATCH] += 1

    return prob / np.maximum(count, 1)
