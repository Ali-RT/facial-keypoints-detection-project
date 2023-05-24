import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import torch

from models import Net


def show_all_keypoints(image, keypoints):
    """Visualize the image and the keypoints on it."""
    plt.figure(figsize=(5, 5))

    keypoints = keypoints.data.numpy() * 55.0 + 95  # adjust keypoint size.
    keypoints = np.reshape(keypoints, (68, -1))  # reshape for proper display on the face

    image = image.numpy()
    image = np.transpose(image, (1, 2, 0))  # convert to numpy image shape (H x W x C)
    image = np.squeeze(image)
    plt.imshow(image, cmap="gray")
    plt.scatter(keypoints[:, 0], keypoints[:, 1], s=40, marker=".", c="m")


def load_image_and_cascade():
    """Load image and Haar cascade classifier."""
    # load in color image for face detection
    image = cv2.imread("images/obamas.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # switch red and blue color channels

    # load in a haar cascade classifier for detecting frontal faces
    face_cascade = cv2.CascadeClassifier("detector_architectures/haarcascade_frontalface_default.xml")

    return image, face_cascade


def detect_faces(image, face_cascade):
    """Detect faces in the image using the Haar cascade classifier."""
    # run the detector
    faces = face_cascade.detectMultiScale(image, 1.2, 2)
    image_with_detections = image.copy()

    # loop over the detected faces, mark the image where each face is found
    for x, y, w, h in faces:
        cv2.rectangle(image_with_detections, (x, y), (x + w, y + h), (255, 0, 0), 3)

    return faces, image_with_detections


def prepare_roi(image, faces):
    """Prepare region of interest (ROI) for each face."""
    image_copy = np.copy(image)

    # loop over the detected faces from your haar cascade
    for x, y, w, h in faces:
        # Select the region of interest that is the face in the image
        roi = image_copy[y : y + h, x : x + w]

        # Normalize the grayscale image so that its color range falls in [0, 1] instead of [0, 255]
        roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY) / 255

        # Rescale the detected face to be the expected square size for your CNN (224x224, suggested)
        roi = cv2.resize(roi, (224, 224))

        # Reshape the numpy image shape (H x W x C) into a torch image shape (C x H x W)
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=0)

        yield torch.from_numpy(roi).type(torch.FloatTensor)


def main():
    """Main function."""
    image, face_cascade = load_image_and_cascade()
    faces, image_with_detections = detect_faces(image, face_cascade)

    net = Net()
    net.load_state_dict(torch.load("./saved_models/facial_keypoints_model_2023_05_22-10_45_56_AM.pt"))
    net.eval()

    for roi_tensor in prepare_roi(image, faces):
        keypoints = net(roi_tensor)
        show_all_keypoints(roi_tensor.squeeze(0), keypoints)

    plt.show()


if __name__ == "__main__":
    main()
