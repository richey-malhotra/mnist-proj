"""
MNIST Digit Recognition Project
Phase 2: Load MNIST Dataset
"""

import warnings
# Suppress irrelevant system warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

from tensorflow.keras.datasets import mnist

def load_data():
    """Load and inspect MNIST dataset."""
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    print(f"Training images: {x_train.shape}")
    print(f"Training labels: {y_train.shape}")
    print(f"Test images: {x_test.shape}")
    print(f"Test labels: {y_test.shape}")
    print(f"Pixel value range: {x_train.min()} to {x_train.max()}")
    
    # Show first few labels to see what they look like
    print(f"First 10 training labels: {y_train[:10]}")
    
    return (x_train, y_train), (x_test, y_test)

def main():
    """Load MNIST data and print information about it."""
    print("Welcome to MNIST Digit Recognition!")
    print("Loading MNIST dataset...\n")
    
    (x_train, y_train), (x_test, y_test) = load_data()
    
    print("\nDataset loaded successfully!")

if __name__ == "__main__":
    main()
