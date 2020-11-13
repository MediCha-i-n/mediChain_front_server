from ..deep_learning import Unet
import numpy as np
from sklearn.feature_extraction.image import extract_patches

def batch(l, n):
    for i in range(0, l.shape[0], n):
        yield l[i:i+n, ::]
def predict(img):
    model = Unet.Unet()
    model.load_weights("best_model.hdf5")

    patch_size = 256
    stride = patch_size//2

    shape = img.shape
    img = np.pad(img, [(stride//2, stride//2), (stride//2, stride//2), (0, 0)], mode = 'reflect')
    pad_shape = img.shape

    pad0 = int(np.ceil(pad_shape[0]/patch_size)*patch_size-pad_shape[0])
    pad1 = int(np.ceil(pad_shape[1]/patch_size)*patch_size-pad_shape[1])

    img = np.pad(img, [(0, pad0), (0, pad1), (0, 0)], mode = 'constant')
    img = extract_patches(img, (patch_size, patch_size, 3), stride)
    patches_shape = img.shape

    img = img.reshape(-1, patch_size, patch_size, 3)

    output = np.zeros((0, patch_size, patch_size))

    for batch_arr in batch(img, 8):
        arr_out = model.predict(batch_arr/255.0)

        arr_out = arr_out.reshape(arr_out[0], arr_out[1], arr_out[2])

        output.append(arr_out, axis = 0)
    output = output.reshape(patches_shape[0], patches_shape[1], patch_size, patch_size)
    output = output[:, :, stride//2:-stride//2, stride//2:-stride//2]

    output = np.concatenate(np.concatenate(output, 1), 1)

    output = output[:shape[0], :shape[1]]

    return output*255










