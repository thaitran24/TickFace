import cv2
import numpy as np
from keras.utils import img_to_array

def l2Normalize(x):
    return x / np.sqrt(np.sum(np.multiply(x, x)))


def normalize(img, normalization='base'):
    if normalization == 'base':
        return img

    # restore input in scale of [0, 255]
    img *= 255 

    if normalization == 'facenet':
        mean, std = img.mean(), img.std()
        img = (img - mean) / std

    elif normalization == 'vggface':
        img[..., 0] -= 93.5940
        img[..., 1] -= 104.7624
        img[..., 2] -= 129.1863

    elif normalization == 'vggface2':
        img[..., 0] -= 91.4953
        img[..., 1] -= 103.8827
        img[..., 2] -= 131.0912

    elif normalization == 'arcface':
        img -= 127.5
        img /= 128
    
    if normalization == 'raw':
        pass 

    return img


def resize(img, target_size):
    if img.shape[0] > 0 and img.shape[1] > 0:
        factor_0 = target_size[0] / img.shape[0]
        factor_1 = target_size[1] / img.shape[1]
        factor = min(factor_0, factor_1)

        dsize = (int(img.shape[1] * factor), int(img.shape[0] * factor))
        img = cv2.resize(img, dsize)

        # pad the other side to the target size by adding black pixels
        diff_0 = target_size[0] - img.shape[0]
        diff_1 = target_size[1] - img.shape[1]

        img = np.pad(img, ((diff_0 // 2, diff_0 - diff_0 // 2), (diff_1 // 2, diff_1 - diff_1 // 2), (0, 0)), 'constant')
        
        if img.shape[0:2] != target_size:
            img = cv2.resize(img, target_size)
        
        # normalize the image
        img_pixels = img_to_array(img)
        img_pixels = np.expand_dims(img_pixels, axis = 0)
        img_pixels /= 255

    return img_pixels


def findThreshold(model_name, distance_metric):
	base_threshold = {'cosine': 0.40, 'euclidean': 0.55, 'euclidean_l2': 0.75}

	thresholds = {
		'vggface':  {'cosine': 0.40, 'euclidean': 0.60, 'euclidean_l2': 0.86},
        'facenet':  {'cosine': 0.40, 'euclidean': 10, 'euclidean_l2': 0.80},
        'arcface':  {'cosine': 0.68, 'euclidean': 4.15, 'euclidean_l2': 1.13},
		'deepface': {'cosine': 0.23, 'euclidean': 64, 'euclidean_l2': 0.64},
        'openface': {'cosine': 0.10, 'euclidean': 0.55, 'euclidean_l2': 0.55},
		'deepid': 	{'cosine': 0.015, 'euclidean': 45, 'euclidean_l2': 0.17}
    }

	threshold = thresholds.get(model_name, base_threshold).get(distance_metric, 0.4)

	return threshold

