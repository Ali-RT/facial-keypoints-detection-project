"""Console script for facial_keypoints_detection."""
import sys
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--data', help='Path to the training data.')
def train(data):
    """
    Train a new model.
    """
    # Call your function to train a model
    # train_model(data)
    click.echo(f"Training model with data from {data}")

@cli.command()
@click.option('--image', help='Path to the image.')
def detect(image):
    """
    Detect facial landmarks in an image.
    """
    # Call your function to detect facial landmarks
    # detect_facial_landmark(image)
    click.echo(f"Detecting facial landmarks in image at {image}")

@cli.command()
@click.option('--image', help='Path to the image.')
@click.option('--filter', help='Filter to be applied.')
def filter(image, filter):
    """
    Apply a filter to a face in an image.
    """
    # Call your function to apply a facial filter
    # apply_facial_filter(image, filter)
    click.echo(f"Applying {filter} to image at {image}")

if __name__ == "__main__":
    cli()
