from utils import *
import numpy as np


def warpPerspective(img: np.ndarray, transform_matrix, output_width, output_height):
    h = img.shape[1]
    w = img.shape[0]
    array = np.zeros([output_width, output_height, 3])
    for i in range(w):
        for j in range(h):
            color = img[i, j]
            x, y = _processWrapImage(i, j, transform_matrix, output_width, output_height)
            if x is None:
                continue
            array[x, y] = color
    return array


def grayScaledFilter(img: np.ndarray):
    img_filter = np.array([[0.33, .33, .33], [0.33, .33, .33], [0.33, .33, .33]])
    return Filter(img, img_filter)


def crazyFilter(img):
    img_filter = np.array([[0, 0, 1], [0, 0.5, 0], [0.5, 0.5, 0]])
    inverted_filter = np.array([[0, -2, 2], [0, 2, 0], [1, 0, 0]])
    crazy_img = Filter(img, img_filter)
    return crazy_img, Filter(crazy_img, inverted_filter)


def scaleImg(img, scale_width, scale_height):
    w = img.shape[0]
    h = img.shape[1]
    array = np.zeros([int(w * scale_width), int(h * scale_height), 3])
    for i in range(w):
        for j in range(h):
            _processScale(img[i, j], array, int(i * scale_width), int(j * scale_height), scale_width, scale_height)
    return array


def _processScale(color, ret, i, j, sw, sh):
    if sw <= 1:
        sw = 1
    if sh <= 1:
        sh = 1
    for x in range(sw):
        for y in range(sh):
            ret[i + x, y + j] = color


def permuteFilter(img):
    img_filter = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    return Filter(img, img_filter)


def _processWrapImage(i, j, transform_matrix: np.ndarray, output_width, output_height):
    v = np.matmul(transform_matrix, np.array([i, j, 1]))
    x = int(v[0] // v[2])
    y = int(v[1] // v[2])
    if 0 <= x < output_width and 0 <= y < output_height:
        return x, y
    return None, None


if __name__ == "__main__":
    image_matrix = get_input('pic.jpg')

    # You can change width and height if you want
    width, height = 300, 400

    showImage(image_matrix, title="Input Image")

    # TODO : Find coordinates of four corners of your inner Image ( X,Y format)
    #  Order of coordinates: Upper Left, Upper Right, Down Left, Down Right
    pts1 = np.float32([[255, 20], [605, 180], [280, 990], [630, 900]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    m = getPerspectiveTransform(pts1, pts2)

    warpedImage = warpPerspective(image_matrix, m, width, height)
    showWarpPerspective(warpedImage)

    grayScalePic = grayScaledFilter(warpedImage)
    showImage(grayScalePic, title="Gray Scaled")

    crazyImage, invertedCrazyImage = crazyFilter(warpedImage)
    showImage(crazyImage, title="Crazy Filter")
    showImage(invertedCrazyImage, title="Inverted Crazy Filter")

    scaledImage = scaleImg(warpedImage, 3, 4)
    showImage(scaledImage, title="Scaled Image")

    permuteImage = permuteFilter(warpedImage)
    showImage(permuteImage, title="Permuted Image")
