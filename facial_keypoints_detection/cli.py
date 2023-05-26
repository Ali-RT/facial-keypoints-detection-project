"""Console script for facial_keypoints_detection."""
import click

from facial_keypoints_detection.apply_facial_filter import apply_filter
from facial_keypoints_detection.detect_facial_keypoints import detect
from facial_keypoints_detection.train_model import train


@click.group()
def cli():
    pass


@cli.command()
@click.option("--data", help="Path to the training data.")
def train_model(data):
    """
    Train a new model.
    """
    # Call your function to train a model
    # train_model(data)
    click.echo(f"Training model with data from {data}")
    train()


@cli.command()
@click.option("--image", help="Path to the image.")
def detect_landmarks(image):
    """
    Detect facial landmarks in an image.
    """
    # Call your function to detect facial landmarks
    # detect_facial_landmark(image)
    click.echo(f"Detecting facial landmarks in image at {image}")
    detect()


@cli.command()
@click.option("--image", help="Path to the image.")
@click.option("--filter", help="Filter to be applied.")
def filter(image, filter):
    """
    Apply a filter to a face in an image.
    """
    # Call your function to apply a facial filter
    # apply_facial_filter(image, filter)
    click.echo(f"Applying {filter} to image at {image}")
    apply_filter()


if __name__ == "__main__":
    cli()
