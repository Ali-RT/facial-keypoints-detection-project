import os

import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def show_keypoints(image, key_pts):
    """Show image with keypoints"""
    plt.imshow(image)
    plt.scatter(key_pts[:, 0], key_pts[:, 1], s=20, marker=".", c="m")


def load_and_process_sunglasses():
    """Load sunglasses image and display its alpha channel"""
    sunglasses = cv2.imread("./images/sunglasses.png", cv2.IMREAD_UNCHANGED)
    alpha_channel = sunglasses[:, :, 3]
    values = np.where(alpha_channel != 0)
    return sunglasses, values


def load_training_data():
    """Load training data and display some basic stats"""
    key_pts_frame = pd.read_csv("./data/training_frames_keypoints.csv")
    return key_pts_frame


def get_image_and_keypoints(n, key_pts_frame):
    """Get an image and its keypoints, based on the index 'n'"""
    image_name = key_pts_frame.iloc[n, 0]
    image = mpimg.imread(os.path.join("./data/training/", image_name))
    key_pts = key_pts_frame.iloc[n, 1:].values
    key_pts = key_pts.astype("float").reshape(-1, 2)
    return image, key_pts


def apply_sunglasses(image, key_pts):
    """Overlay sunglasses on an image based on keypoints"""
    image_copy = np.copy(image)

    # Position of sunglasses: between the eyebrows and over the nose
    x = int(key_pts[17, 0])
    y = int(key_pts[17, 1])
    h = int(abs(key_pts[27, 1] - key_pts[34, 1]))
    w = int(abs(key_pts[17, 0] - key_pts[26, 0]))

    sunglasses, _ = load_and_process_sunglasses()
    new_sunglasses = cv2.resize(sunglasses, (w, h), interpolation=cv2.INTER_CUBIC)

    # get region of interest on the face to change
    roi_color = image_copy[y : y + h, x : x + w]

    # find all non-transparent pts
    ind = np.argwhere(new_sunglasses[:, :, 3] > 0)

    # for each non-transparent point, replace the original image pixel with that of the new_sunglasses
    for i in range(3):
        roi_color[ind[:, 0], ind[:, 1], i] = new_sunglasses[ind[:, 0], ind[:, 1], i]
    image_copy[y : y + h, x : x + w] = roi_color

    return image_copy


if __name__ == "__main__":
    sunglasses, values = load_and_process_sunglasses()
    print("The non-zero values of the alpha channel are: ", values)

    key_pts_frame = load_training_data()
    print("Number of images: ", key_pts_frame.shape[0])

    n = 120  # index of image to use
    image, key_pts = get_image_and_keypoints(n, key_pts_frame)
    print("Image name: ", key_pts_frame.iloc[n, 0])

    plt.figure(figsize=(5, 5))
    show_keypoints(image, key_pts)
    plt.show()

    image_with_sunglasses = apply_sunglasses(image, key_pts)
    plt.imshow(image_with_sunglasses)
    plt.show()
