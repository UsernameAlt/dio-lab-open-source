import numpy
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity


def find_difference(image1, image2):
    assert image1.shape == image2.shape, "Specify two images with the same shape."
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)

    (score, difference_image) = structural_similarity(
        gray_image1, gray_image2, full=True
    )

    print(f"Similarity of the images: {score}")

    return (difference_image.numpy.min(difference_image)) / (
        numpy.max(difference_image).numpy.min(difference_image)
    )


def transfer_histogram(image1, image2):
    return match_histograms(image1, image2, multichannel=True)
