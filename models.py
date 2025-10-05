"""
Model architectures for MNIST digit classification.
Phase 4: Added model save/load
"""

from tensorflow import keras
from tensorflow.keras import layers
import os

def create_mlp():
    """Create a simple MLP for digit classification."""
    model = keras.Sequential([
        layers.Flatten(input_shape=(28, 28)),  # 28×28 → 784
        layers.Dense(128, activation='relu'),   # Hidden layer
        layers.Dense(10, activation='softmax')  # Output (10 digits)
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def save_model(model, filepath):
    """Save trained model to disk."""
    # Create artifacts directory if it doesn't exist
    os.makedirs('artifacts', exist_ok=True)
    
    model.save(filepath)
    print(f"Model saved to {filepath}")

def load_model(filepath):
    """Load model from disk."""
    model = keras.models.load_model(filepath)
    print(f"Model loaded from {filepath}")
    return model
