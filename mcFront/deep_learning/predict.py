from ..deep_learning import Unet
import os
import numpy as np
import cv2
from sklearn.feature_extraction.image import extract_patches

def batch(l, n):
    for i in range(0, l.shape[0], n):
        yield l[i:i+n, ::]
def predict(img):
    model = Unet.Unet()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model.load_weights(os.path.join(BASE_DIR, "best_model.hdf5"))

    shape = img.shape

    img = cv2.resize(img, (256, 256)).reshape(1, 256, 256, 3)
    output = model.predict(img)
    output = np.around(output)

    output = output.reshape(256, 256)

    output = cv2.resize(output, (shape[1], shape[0]), interpolation=cv2.INTER_CUBIC)

    return output * 255










