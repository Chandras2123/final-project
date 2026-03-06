import numpy as np
import cv2
import tensorflow as tf

CLASSIFIER_PATH = "classifier_model.keras"
clf_model = tf.keras.models.load_model(CLASSIFIER_PATH)

CLASS_NAMES = ["glioma", "meningioma", "pituitary", "no_tumor"]


def classify_image(img):

    # Resize
    img = cv2.resize(img, (224, 224))

    # If grayscale, convert to 3 channels
    if len(img.shape) == 2:
        img = np.stack((img,) * 3, axis=-1)

    # Ensure shape is (224,224,3)
    img = img.astype("float32")

    # Add batch dimension ONLY ONCE
    img = np.expand_dims(img, axis=0)

    pred = clf_model.predict(img, verbose=0)
    class_id = np.argmax(pred)

    return CLASS_NAMES[class_id]


def classify_slices(volume):

    predictions = []

    for z in range(volume.shape[2]):

        slice_img = volume[:, :, z]

        if np.sum(slice_img) < 1e-3:
            continue

        slice_img = cv2.resize(slice_img, (224, 224))

        # Convert grayscale to RGB
        slice_img = np.stack((slice_img,) * 3, axis=-1)

        slice_img = slice_img.astype("float32")
        slice_img = np.expand_dims(slice_img, axis=0)

        pred = clf_model.predict(slice_img, verbose=0)
        class_id = np.argmax(pred)

        predictions.append(class_id)

    if len(predictions) == 0:
        return "no_tumor"

    final_class = max(set(predictions), key=predictions.count)

    return CLASS_NAMES[final_class]