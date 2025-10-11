"""
MNIST Digit Recognition Project
Phase 5: Make Predictions
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

from tensorflow.keras.datasets import mnist
import numpy as np
from models import create_mlp, save_model, load_model, predict_digit
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

def test_predictions(model, x_test_raw, y_test, num_samples=5):
    """Try the model on some random test images and print results."""
    print(f"\nTesting predictions on {num_samples} random images...")
    print("-" * 50)
    
    # Pick random indices
    indices = np.random.choice(len(x_test_raw), num_samples, replace=False)
    
    correct = 0
    for i, idx in enumerate(indices):
        # Get image and true label
        image = x_test_raw[idx]
        true_label = y_test[idx]
        
        # Make prediction
        predicted_digit, confidence = predict_digit(model, image)
        
        # Check if correct
        is_correct = predicted_digit == true_label
        if is_correct:
            correct += 1
        
        # Display result
        status = "✓" if is_correct else "✗"
        print(f"{status} Image {i+1}: Predicted={predicted_digit}, "
              f"Actual={true_label}, Confidence={confidence:.1f}%")
    
    print("-" * 50)
    print(f"Accuracy: {correct}/{num_samples} correct ({correct/num_samples*100:.0f}%)")

def main():
    """Train or load model, then test predictions."""
    print("Welcome to MNIST Digit Recognition!")
    print("Phase 5: Making Predictions\n")
    
    model_path = 'artifacts/mnist_mlp.keras'
    
    # Load raw data for predictions (need unnormalised images)
    print("Loading MNIST dataset...")
    (x_train_raw, y_train), (x_test_raw, y_test) = mnist.load_data()
    
    # Load normalised data for training/evaluation
    (x_train, _), (x_test, _) = load_data()
    
    # Check if saved model exists
    if os.path.exists(model_path):
        print(f"\nFound existing model at {model_path}")
        choice = input("Load existing model? (y/n): ").strip().lower()
        
        if choice == 'y':
            model = load_model(model_path)
            print("\nModel loaded successfully!")
            
            # Evaluate loaded model
            print("\nEvaluating loaded model...")
            loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
            print(f"Test accuracy: {accuracy*100:.2f}%")
            
            # Test predictions
            test_predictions(model, x_test_raw, y_test, num_samples=5)
            return
    
    # Train new model
    print("\nTraining new model...")
    
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
    
    # Test predictions on trained model
    test_predictions(model, x_test_raw, y_test, num_samples=5)
    
    print("\nDone! Model can make predictions on new images.")

if __name__ == "__main__":
    main()
