from datetime import datetime

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms

from data_load import (
    FacialKeypointsDataset,
    Normalize,
    RandomCrop,
    Rescale,
    ToTensor,
)
from models import Net


def get_transforms() -> transforms.Compose:
    """Creates a composition of image transformations."""
    return transforms.Compose([Rescale(250), RandomCrop(224), Normalize(), ToTensor()])


def get_dataloaders(batch_size_train: int, batch_size_test: int) -> (DataLoader, DataLoader):
    """Generates train and test data loaders."""
    data_transform = get_transforms()

    train_dataset = FacialKeypointsDataset(
        csv_file="./data/training_frames_keypoints.csv",
        root_dir="./data/training/",
        transform=data_transform,
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size_train, shuffle=True, num_workers=0)

    test_dataset = FacialKeypointsDataset(
        csv_file="./data/test_frames_keypoints.csv",
        root_dir="./data/test/",
        transform=data_transform,
    )

    test_loader = DataLoader(test_dataset, batch_size=batch_size_test, shuffle=True, num_workers=0)

    return train_loader, test_loader


def validate_model(model: nn.Module, criterion: nn.Module, test_loader: DataLoader) -> float:
    """Returns the validation loss for the given model on test data."""
    validation_loss = 0.0
    model.eval()  # Set the model to evaluation mode

    with torch.no_grad():  # Turn off gradients for validation to save memory and computations
        for sample in test_loader:
            images, keypoints = (
                sample["image"].float(),
                sample["keypoints"].view(sample["keypoints"].size(0), -1).float(),
            )
            outputs = model(images)
            loss = criterion(outputs, keypoints)
            validation_loss += loss.item()

    return validation_loss


def train_model(
    model: nn.Module,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    train_loader: DataLoader,
    test_loader: DataLoader,
    num_epochs: int,
) -> None:
    """Train the model and print loss statistics."""
    print_interval = 10
    for epoch in range(num_epochs):
        running_loss = 0.0

        # Train on batches of data
        for batch_idx, data in enumerate(train_loader):
            # Clear the gradients
            optimizer.zero_grad()

            # Forward pass, backward pass, optimize
            images, keypoints = (
                data["image"].float(),
                data["keypoints"].view(data["keypoints"].size(0), -1).float(),
            )
            outputs = model(images)
            loss = criterion(outputs, keypoints)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if batch_idx % print_interval == 0:
                validation_loss = validate_model(model, criterion, test_loader)
                print(
                    f"Epoch: {epoch + 1}/{num_epochs}, Batch: {batch_idx}, Training Loss: {running_loss / print_interval:.5f}, "
                    f"Validation Loss: {validation_loss / len(test_loader):.5f}"
                )
                running_loss = 0.0
        # End of epoch

    print("Finished training.")


def main() -> None:
    """Main function."""
    model = Net()
    criterion = nn.SmoothL1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    train_loader, test_loader = get_dataloaders(batch_size_train=32, batch_size_test=10)

    train_model(model, criterion, optimizer, train_loader, test_loader, num_epochs=5)

    # Save the model
    date_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")  # Get current date and time
    model_name = f"./saved_models/facial_keypoints_model_{date_time}.pth"  # Create a unique name for the model
    torch.save(model.state_dict(), model_name)
    print(f"Model saved as {model_name}")


if __name__ == "__main__":
    main()
