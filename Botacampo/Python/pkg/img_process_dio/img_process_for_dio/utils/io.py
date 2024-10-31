from skimage.io import imread, imsave


def read_image(path, is_gray=False):
    return imread(path, as_gray=is_gray)


def save_image(image, path):
    imsave(path, image)
