"""
MNIST Digit Recognition Project
Phase 4: Save and Load Models
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

from tensorflow.keras.datasets import mnist
import numpy as np
from models import create_mlp, save_model, load_model
import os

def load_data():
    """Load and normalise MNIST dataset."""
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    
    # Normalise pixel values from 0-255 to 0-1
    x_train = x_train / 255.0
    x_test = x_test / 255.0
    
    print(f"Training images: {x_train.shape}")
    print(f"Test images: {x_test.shape}")
    print(f"Pixel range: {x_train.min():.1f} to {x_train.max():.1f}")
    
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
    """Train model and save it, or load existing model."""
    print("Welcome to MNIST Digit Recognition!")
    print("Phase 4: Model Persistence\n")
    
    model_path = 'artifacts/mnist_mlp.keras'
    
    # Check if saved model exists
    if os.path.exists(model_path):
        print(f"Found existing model at {model_path}")
        choice = input("Load existing model? (y/n): ").strip().lower()
        
        if choice == 'y':
            model = load_model(model_path)
            print("\nModel loaded successfully!")
            
            # Load test data to evaluate
            print("\nLoading test data...")
            (x_train, y_train), (x_test, y_test) = load_data()
            
            # Evaluate loaded model
            print("\nEvaluating loaded model...")
            loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
            print(f"Test accuracy: {accuracy*100:.2f}%")
            return
    
    # Train new model
    print("Training new model...\n")
    
    # Load and normalise data
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = load_data()
    
    # Create model
    print("\nCreating MLP model...")
    model = create_mlp()
    
    # Train model
    history = train_model(model, x_train, y_train, x_test, y_test, epochs=3)
    
    # Show final accuracy
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    
    print(f"\nTraining complete!")
    print(f"Final training accuracy: {final_train_acc*100:.2f}%")
    print(f"Final validation accuracy: {final_val_acc*100:.2f}%")
    
    # Save the trained model
    print(f"\nSaving model to {model_path}...")
    save_model(model, model_path)
    print("Done! Model can be loaded later without retraining.")

if __name__ == "__main__":
    main()
