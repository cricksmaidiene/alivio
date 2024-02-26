import numpy as np
import cv2

#### Augmentations
def shift_image(img, shift_pnt):
    M = np.float32([[1, 0, shift_pnt[0]], [0, 1, shift_pnt[1]]])
    res = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), borderMode=cv2.BORDER_REFLECT_101)
    return res


def rotate_image(image, angle, scale, rot_pnt):
    rot_mat = cv2.getRotationMatrix2D(rot_pnt, angle, scale)
    result = cv2.warpAffine(image, rot_mat, (image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101) #INTER_NEAREST
    return result


def gauss_noise(img, var=30):
    row, col, ch = img.shape
    mean = var
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    gauss = (gauss - np.min(gauss)).astype(np.uint8)
    return np.clip(img.astype(np.int32) + gauss, 0, 255).astype('uint8')


def clahe(img, clipLimit=2.0, tileGridSize=(5,5)):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_LAB2RGB)
    return img_output


def _blend(img1, img2, alpha):
    return np.clip(img1 * alpha + (1 - alpha) * img2, 0, 255).astype('uint8')


_alpha = np.asarray([0.114, 0.587, 0.299]).reshape((1, 1, 3))
def _grayscale(img):
    return np.sum(_alpha * img, axis=2, keepdims=True)


def saturation(img, alpha):
    gs = _grayscale(img)
    return _blend(img, gs, alpha)


def brightness(img, alpha):
    gs = np.zeros_like(img)
    return _blend(img, gs, alpha)


def contrast(img, alpha):
    gs = _grayscale(img)
    gs = np.repeat(gs.mean(), 3)
    return _blend(img, gs, alpha)


def change_hsv(img, h, s, v):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(int)
    hsv[:,:,0] += h
    hsv[:,:,0] = np.clip(hsv[:,:,0], 0, 255)
    hsv[:,:,1] += s
    hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
    hsv[:,:,2] += v
    hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
    hsv = hsv.astype('uint8')
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def shift_channels(img, b_shift, g_shift, r_shift):
    img = img.astype(int)
    img[:,:,0] += b_shift
    img[:,:,0] = np.clip(img[:,:,0], 0, 255)
    img[:,:,1] += g_shift
    img[:,:,1] = np.clip(img[:,:,1], 0, 255)
    img[:,:,2] += r_shift
    img[:,:,2] = np.clip(img[:,:,2], 0, 255)
    img = img.astype('uint8')
    return img
    
def invert(img):
    return 255 - img

def channel_shuffle(img):
    ch_arr = [0, 1, 2]
    np.random.shuffle(ch_arr)
    img = img[..., ch_arr]
    return img
    
#######


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count



def preprocess_inputs(x):
    x = np.asarray(x, dtype='float32')
    x /= 127
    x -= 1
    return x


def dice(im1, im2, empty_score=1.0):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.
    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
        Both are empty (sum eq to zero) = empty_score

    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.
    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_score

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / im_sum


def iou(im1, im2, empty_score=1.0):
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    union = np.logical_or(im1, im2)
    im_sum = union.sum()
    if im_sum == 0:
        return empty_score

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return intersection.sum() / im_sum

def flip(img, flip_direction = 'vertical'):
    # Flip the image based on the specified direction
    if flip_direction == 'vertical':
        flipped_image = cv2.flip(img, 0)
    elif flip_direction == 'horizontal':
        flipped_image = cv2.flip(img, 1)
    else:
        raise ValueError("Invalid flip_direction. Use 'vertical' or 'horizontal'.")

    return flipped_image

def zoom_image(img, zoom_factor=1.0):
    # Get the original image dimensions
    original_height, original_width = img.shape[:2]

    # Calculate the new dimensions based on the zoom factor
    new_height = int(original_height * zoom_factor)
    new_width = int(original_width * zoom_factor)

    # Resize the image
    zoomed_image = cv2.resize(img, (new_width, new_height))

    return zoomed_image

def random_crop_image(img, crop_percentage=0.8):
    """
    Randomly crop a section of the image.

    Parameters:
    - image_path (str): Path to the image file.
    - crop_percentage (float): Percentage of the image to be retained after cropping.
                              Values should be in the range (0.0, 1.0). Default is 0.8 (80%).

    Returns:
    - cropped_image (numpy.ndarray): Cropped image as a NumPy array.
    """

    # Get the original image dimensions
    original_height, original_width = img.shape[:2]

    # Calculate the crop dimensions
    crop_height = int(original_height * crop_percentage)
    crop_width = int(original_width * crop_percentage)

    # Randomly choose starting pts for top-left corner of crop
    start_y = np.random.randint(0, original_height - crop_height + 1)
    start_x = np.random.randint(0, original_width - crop_width + 1)

    # Crop the image
    cropped_image = img[start_y:start_y + crop_height, start_x:start_x + crop_width]

    return cropped_image