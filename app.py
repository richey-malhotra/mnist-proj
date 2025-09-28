"""
MNIST Digit Recognition Project
Phase 3: Train First MLP Model
"""

import warnings
# Suppress irrelevant system warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

from tensorflow.keras.datasets import mnist
import numpy as np
from models import create_mlp

def load_data():
    """Load and normalise MNIST dataset."""
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalise pixel values from 0-255 to 0-1
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    
    print(f"Training images: {x_train.shape}")
    print(f"Training labels: {y_train.shape}")
    print(f"Test images: {x_test.shape}")
    print(f"Test labels: {y_test.shape}")
    print(f"Pixel value range after normalisation: {x_train.min():.1f} to {x_train.max():.1f}")
    
    return (x_train, y_train), (x_test, y_test)

def train_model(model, x_train, y_train, x_test, y_test, epochs=3):
    """Train the model and return history."""
    print(f"\nTraining for {epochs} epochs...")
    
    history = model.fit(
        x_train, y_train,
        epochs=epochs,
        batch_size=32,
        validation_data=(x_test, y_test),
        verbose=1
    )
    
    return history

def main():
    """Load data, create model, and train it."""
    print("Welcome to MNIST Digit Recognition!")
    print("Phase 3: Training MLP Model\n")
    
    # Load and normalise data
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_data()
    
    # Create model
    print("\nCreating MLP model...")
    model = create_mlp()
    model.summary()
    
    # Train model
    history = train_model(model, x_train, y_train, x_test, y_test, epochs=3)
    
    # Show final accuracy
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    
    print(f"\nTraining complete!")
    print(f"Final training accuracy: {final_train_acc*100:.2f}%")
    print(f"Final validation accuracy: {final_val_acc*100:.2f}%")

if __name__ == "__main__":
    main()
